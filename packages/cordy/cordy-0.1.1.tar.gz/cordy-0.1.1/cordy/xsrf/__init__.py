# The following code is adapted from Django
import re
import string

from cordy.utils import get_random_string, constant_time_compare


CSRF_SECRET_LENGTH = 32
CSRF_TOKEN_LENGTH = 2 * CSRF_SECRET_LENGTH
CSRF_ALLOWED_CHARS = string.ascii_letters + string.digits
CSRF_SESSION_KEY = '_csrftoken'


def _get_new_csrf_string():
    return get_random_string(CSRF_SECRET_LENGTH, allowed_chars=CSRF_ALLOWED_CHARS)


def _mask_cipher_secret(secret):
    """
    Given a secret (assumed to be a string of CSRF_ALLOWED_CHARS), generate a
    token by adding a mask and applying it to the secret.
    """
    mask = _get_new_csrf_string()
    chars = CSRF_ALLOWED_CHARS
    pairs = zip((chars.index(x) for x in secret), (chars.index(x) for x in mask))
    cipher = ''.join(chars[(x + y) % len(chars)] for x, y in pairs)
    return mask + cipher


def _unmask_cipher_token(token):
    """
    Given a token (assumed to be a string of CSRF_ALLOWED_CHARS, of length
    CSRF_TOKEN_LENGTH, and that its first half is a mask), use it to decrypt
    the second half to produce the original secret.
    """
    mask = token[:CSRF_SECRET_LENGTH]
    token = token[CSRF_SECRET_LENGTH:]
    chars = CSRF_ALLOWED_CHARS
    pairs = zip((chars.index(x) for x in token), (chars.index(x) for x in mask))
    return ''.join(chars[x - y] for x, y in pairs)  # Note negative values are ok


def _get_new_csrf_token():
    return _mask_cipher_secret(_get_new_csrf_string())


def get_token(request):
    """
    Return the CSRF token required for a POST form. The token is an
    alphanumeric value. A new token is created if one is not already set.
    A side effect of calling this function is to make the csrf_protect
    decorator and the CsrfViewMiddleware add a CSRF cookie and a 'Vary: Cookie'
    header to the outgoing response.  For this reason, you may need to use this
    function lazily, as is done by the csrf context processor.
    """
    if "CSRF_COOKIE" not in request.META:
        csrf_secret = _get_new_csrf_string()
        request.META["CSRF_COOKIE"] = _mask_cipher_secret(csrf_secret)
    else:
        csrf_secret = _unmask_cipher_token(request.META["CSRF_COOKIE"])
    request.META["CSRF_COOKIE_USED"] = True
    return _mask_cipher_secret(csrf_secret)


def rotate_token(request):
    """
    Change the CSRF token in use for a request - should be done on login
    for security purposes.
    """
    request.META.update({
        "CSRF_COOKIE_USED": True,
        "CSRF_COOKIE": _get_new_csrf_token(),
    })
    request.csrf_cookie_needs_reset = True


def _sanitize_token(token):
    # Allow only ASCII alphanumerics
    if re.search('[^a-zA-Z0-9]', token):
        return _get_new_csrf_token()
    elif len(token) == CSRF_TOKEN_LENGTH:
        return token
    elif len(token) == CSRF_SECRET_LENGTH:
        # Older Django versions set cookies to values of CSRF_SECRET_LENGTH
        # alphanumeric characters. For backwards compatibility, accept
        # such values as unmasked secrets.
        # It's easier to mask here and be consistent later, rather than add
        # different code paths in the checks, although that might be a tad more
        # efficient.
        return _mask_cipher_secret(token)
    return _get_new_csrf_token()


def _compare_masked_tokens(request_csrf_token, csrf_token):
    # Assume both arguments are sanitized -- that is, strings of
    # length CSRF_TOKEN_LENGTH, all CSRF_ALLOWED_CHARS.
    return constant_time_compare(
        _unmask_cipher_token(request_csrf_token),
        _unmask_cipher_token(csrf_token),
    )



