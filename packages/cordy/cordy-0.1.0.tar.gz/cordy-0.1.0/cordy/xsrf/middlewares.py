# This code is largely inspired (and copied) from Django
from collections import defaultdict
from urllib.parse import urlparse

from cached_property import cached_property

from cordy.base.exceptions import ImproperlyConfigured
from cordy.conf import settings
from cordy.middlewares import BaseMiddleware
from cordy.utils import patch_vary_headers, is_same_domain
from cordy.xsrf import _compare_masked_tokens, _sanitize_token, CSRF_SESSION_KEY, get_token
from cordy.xsrf.exceptions import (XSRFMissing, XSRFTokenInvalid, XSRFNoReferer, XSRFBadOrigin,
                                   XSRFMalformedReferer, XSRFInsecureReferer, XSRFBadReferer)


class XSRFMiddleware(BaseMiddleware):

    @cached_property
    def csrf_trusted_origins_hosts(self):
        return [
            urlparse(origin).netloc.lstrip('*')
            for origin in settings.CSRF_TRUSTED_ORIGINS
        ]

    @cached_property
    def allowed_origins_exact(self):
        return {
            origin for origin in settings.CSRF_TRUSTED_ORIGINS
            if '*' not in origin
        }

    @cached_property
    def allowed_origin_subdomains(self):
        """
        A mapping of allowed schemes to list of allowed netlocs, where all
        subdomains of the netloc are allowed.
        """
        allowed_origin_subdomains = defaultdict(list)
        for parsed in (urlparse(origin) for origin in settings.CSRF_TRUSTED_ORIGINS if '*' in origin):
            allowed_origin_subdomains[parsed.scheme].append(parsed.netloc.lstrip('*'))
        return allowed_origin_subdomains

    # The _accept method currently only exist for the sake of the
    # requires_csrf_token decorator.
    def _accept(self):
        # Avoid checking the request twice by adding a custom attribute to
        # request.  This will be relevant when both decorator and middleware
        # are used.
        self.request.csrf_processing_done = True
        super().after_request(self.request)

    def _get_token(self):
        request = self.request

        if settings.CSRF_USE_SESSIONS:
            try:
                return request.session.get(CSRF_SESSION_KEY)
            except AttributeError:
                raise ImproperlyConfigured(
                    'CSRF_USE_SESSIONS is enabled, but request.session is not '
                    'set. SessionMiddleware must appear before CsrfViewMiddleware '
                    'in MIDDLEWARE.'
                )

        try:
            cookie_token = request.cookies[settings.CSRF_COOKIE_NAME]
        except KeyError:
            return None

        csrf_token = _sanitize_token(cookie_token)
        if csrf_token != cookie_token:
            # Cookie token needed to be replaced;
            # the cookie needs to be reset.
            request.csrf_cookie_needs_reset = True
        return csrf_token

    def _set_token(self):
        request = self.request

        if settings.CSRF_USE_SESSIONS:
            if request.session.get(CSRF_SESSION_KEY) != request.META['CSRF_COOKIE']:
                request.session[CSRF_SESSION_KEY] = request.META['CSRF_COOKIE']
                request.session.save()
        else:
            response = self.response

            response.set_cookie(
                settings.CSRF_COOKIE_NAME,
                request.META.get('CSRF_COOKIE', get_token(request)),
                max_age=settings.CSRF_COOKIE_AGE,
                domain=settings.CSRF_COOKIE_DOMAIN,
                path=settings.CSRF_COOKIE_PATH,
                secure=settings.CSRF_COOKIE_SECURE,
                httponly=settings.CSRF_COOKIE_HTTPONLY,
                samesite=settings.CSRF_COOKIE_SAMESITE,
            )
            # Set the Vary header since content varies with the CSRF cookie.
            patch_vary_headers(response, ('Cookie',))

    def _origin_verified(self, request):
        request_origin = request.origin()
        good_host = request.host()
        good_origin = '%s://%s' % (
            'https' if request.is_secure() else 'http',
            good_host,
        )
        if request_origin == good_origin:
            return True

        if request_origin in self.allowed_origins_exact:
            return True
        try:
            parsed_origin = urlparse(request_origin)
        except ValueError:
            return False
        request_scheme = parsed_origin.scheme
        request_netloc = parsed_origin.netloc
        return any(
            is_same_domain(request_netloc, host)
            for host in self.allowed_origin_subdomains.get(request_scheme, ())
        )

    def after_request(self, request):
        self.request = request

        if settings.USE_CSRF is False:
            return self._accept()

        csrf_token = self._get_token()
        if csrf_token is not None:
            # Use same token next time.
            request.META['CSRF_COOKIE'] = csrf_token
        if self.request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            return self._accept()

        if getattr(request, '_dont_enforce_csrf_checks', False):
            return self._accept()

        # Reject the request if the Origin header doesn't match an allowed
        # value.
        if request.origin() is not None:
            if not self._origin_verified(request):
                raise XSRFBadOrigin(request.origin())
        elif request.is_secure():
            # If the Origin header wasn't provided, reject HTTPS requests
            # if the Referer header doesn't match an allowed value.
            #
            # Suppose user visits http://example.com/
            # An active network attacker (man-in-the-middle, MITM) sends a
            # POST form that targets https://example.com/detonate-bomb/ and
            # submits it via JavaScript.
            #
            # The attacker will need to provide a CSRF cookie and token, but
            # that's no problem for a MITM and the session-independent
            # secret we're using. So the MITM can circumvent the CSRF
            # protection. This is true for any HTTP connection, but anyone
            # using HTTPS expects better! For this reason, for
            # https://example.com/ we need additional protection that treats
            # http://example.com/ as completely untrusted. Under HTTPS,
            # Barth et al. found that the Referer header is missing for
            # same-domain requests in only about 0.2% of cases or less, so
            # we can use strict Referer checking.
            referer = request.referer
            if referer is None:
                raise XSRFNoReferer

            try:
                referer = urlparse(referer)
            except ValueError:
                raise XSRFMalformedReferer

            # Make sure we have a valid URL for Referer.
            if '' in (referer.scheme, referer.netloc):
                raise XSRFMalformedReferer

            # Ensure that our Referer is also secure.
            if referer.scheme != 'https':
                raise XSRFInsecureReferer

            good_referer = (
                settings.SESSION_COOKIE_DOMAIN
                if settings.CSRF_USE_SESSIONS
                else settings.CSRF_COOKIE_DOMAIN
            )
            if good_referer is None:
                # If no cookie domain is configured, allow matching the
                # current host:port exactly if it's permitted by
                # ALLOWED_HOSTS.
                good_referer = request.host()
            else:
                server_port = request.host_port
                if server_port not in ('443', '80'):
                    good_referer = '%s:%s' % (good_referer, server_port)

             # Create an iterable of all acceptable HTTP referers.
            good_hosts = self.csrf_trusted_origins_hosts
            if good_referer is not None:
                good_hosts = (*good_hosts, good_referer)

            if not any(is_same_domain(referer.netloc, host) for host in good_hosts):
                raise XSRFBadReferer

        csrf_token = self._get_token()
        if csrf_token is None:
            # No CSRF cookie. For POST requests, we insist on a CSRF cookie,
            # and in this way we can avoid all CSRF attacks, including login
            # CSRF.
            raise XSRFMissing

        # Check non-cookie token for match.
        request_csrf_token = ""
        if request.method == "POST":
            try:
                request_csrf_token = request.POST.get('csrfmiddlewaretoken', '')
            except OSError:
                # Handle a broken connection before we've completed reading
                # the POST data. process_view shouldn't raise any
                # exceptions, so we'll ignore and serve the user a 403
                # (assuming they're still listening, which they probably
                # aren't because of the error).
                pass

        if request_csrf_token == "":
            # Fall back to X-CSRFToken, to make things easier for AJAX,
            # and possible for PUT/DELETE.
            request_csrf_token = request.headers.get(settings.CSRF_HEADER_NAME, '')

        request_csrf_token = _sanitize_token(request_csrf_token)
        if not _compare_masked_tokens(request_csrf_token, csrf_token):
            raise XSRFTokenInvalid

        return self._accept()

    def after_response(self):
        response = self.response
        request = self.request
        skip = False

        if not getattr(request, 'csrf_cookie_needs_reset', False):
            if getattr(response, 'csrf_cookie_set', False):
                skip = True

        # if not request.META.get("CSRF_COOKIE_USED", False):
        #     skip = True

        if not skip:
            # Set the CSRF cookie even if it's already set, so we renew
            # the expiry timer.
            self._set_token()
            response.csrf_cookie_set = True

        return super().after_response()
