from decimal import Decimal
import datetime
import hashlib
from importlib import import_module
import re
import secrets
import string

from routes.route import Route


RANDOM_STRING_CHARS = string.ascii_letters + string.digits


## Copied from django
def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError('Module "%s" does not define a "%s" attribute/class' % (
            module_path, class_name)
        ) from err


NOT_PROVIDED = object()


## Copied from django
def get_random_string(length=NOT_PROVIDED, allowed_chars=RANDOM_STRING_CHARS):
    """
    Return a securely generated random string.

    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)

    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    if length is NOT_PROVIDED:
        length = 12
    return ''.join(secrets.choice(allowed_chars) for i in range(length))


## Copied from django
_PROTECTED_TYPES = (
    type(None), int, float, Decimal, datetime.datetime, datetime.date, datetime.time,
)


## Copied from django
def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_str(strings_only=True).
    """
    return isinstance(obj, _PROTECTED_TYPES)


## Copied from django
def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and is_protected_type(s):
        return s
    if isinstance(s, memoryview):
        return bytes(s)
    return str(s).encode(encoding, errors)


## Copied from django
def pbkdf2(password, salt, iterations, dklen=0, digest=None):
    """Return the hash of password using pbkdf2."""
    if digest is None:
        digest = hashlib.sha256
    dklen = dklen or None
    password = force_bytes(password)
    salt = force_bytes(salt)
    return hashlib.pbkdf2_hmac(digest().name, password, salt, iterations, dklen)


## Copied from django
def constant_time_compare(val1, val2):
    """Return True if the two strings are equal, False otherwise."""
    return secrets.compare_digest(force_bytes(val1), force_bytes(val2))


def CrudAPI(name, controller):
    print(name)
    return [
        Route(f'{name}_list', f'/{name}/', controller=controller, action='index', conditions={'method': ['GET']}),
        Route(f'{name}_create', f'/{name}/', controller=controller, action='create', conditions={'method': ['POST']}),
        Route(f'{name}_detail', f'/{name}/' + '{id}/', controller=controller, action='get',
              conditions={'method': ['GET']}),
        Route(f'{name}_update', f'/{name}/' + '{id}/', controller=controller, action='update',
              conditions={'method': ['PUT', 'PATCH']}),
        Route(f'{name}_delete', f'/{name}/' + '{id}/', controller=controller, action='delete',
              conditions={'method': ['DELETE']}),
    ]


def include(urls, prefix):
    return urls, prefix


def get_uwsgi():
    try:
        import uwsgi
    except ModuleNotFoundError:
        # The uwsgi module is exported by the uwsgi process itself through the python plugin.
        # This is a shell or test environment
        import cordy.testing.uwsgi_mock as uwsgi

    return uwsgi


## Adapted from Django
def patch_vary_headers(response, newheaders):
    """
    Add (or update) the "Vary" header in the given HttpResponse object.
    newheaders is a list of header names that should be in "Vary". If headers
    contains an asterisk, then "Vary" header will consist of a single asterisk
    '*'. Otherwise, existing headers in "Vary" aren't removed.
    """
    # Note that we need to keep the original order intact, because cache
    # implementations may rely on the order of the Vary contents in, say,
    # computing an MD5 hash.
    if 'Vary' in response.headers:
        cc_delim_re = re.compile(r'\s*,\s*', 0)
        vary_headers = cc_delim_re.split(response.headers['Vary'])
    else:
        vary_headers = []
    # Use .lower() here so we treat headers as case-insensitive.
    existing_headers = {header.lower() for header in vary_headers}
    additional_headers = [newheader for newheader in newheaders
                          if newheader.lower() not in existing_headers]
    vary_headers += additional_headers
    if '*' in vary_headers:
        response.headers['Vary'] = '*'
    else:
        response.headers['Vary'] = ', '.join(vary_headers)


## Copied from django
def is_same_domain(host, pattern):
    """
    Return ``True`` if the host is either an exact match or a match
    to the wildcard pattern.
    Any pattern beginning with a period matches a domain and all of its
    subdomains. (e.g. ``.example.com`` matches ``example.com`` and
    ``foo.example.com``). Anything else is an exact string match.
    """
    if not pattern:
        return False

    pattern = pattern.lower()
    return (
        pattern[0] == '.' and (host.endswith(pattern) or host == pattern[1:]) or
        pattern == host
    )
