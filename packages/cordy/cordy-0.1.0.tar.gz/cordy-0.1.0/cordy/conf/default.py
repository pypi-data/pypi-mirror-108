# SIMPLE SETTINGS

SIMPLE_SETTINGS = {
    'OVERRIDE_BY_ENV': True,
    'CONFIGURE_LOGGING': True,
    'REQUIRED_SETTINGS': [
        'DEBUG',
        'URLS',
        'SECRET_KEY',
    ],
}


# GENERAL

INSTALLED_APPS = [
    'cordy',
]

MIDDLEWARES = [
    'cordy.middlewares.session.SessionMiddleware',
    'cordy.auth.middlewares.SessionMiddleware',
]

URLS = 'urls'
DOCUMENT_API = False

# TEMPLATES

USES_TEMPLATES = None
TEMPLATE_DIRS = [
    'templates',
]
TEMPLATES_FROM_APP = True
TEMPLATES_JINJA_EXTENSIONS = []

# DATABASE

DATABASE = None

# LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'loggers': {
    #     '': {
    #         'level': 'DEBUG',
    #         'propagate': True,
    #     },
    # }
}

USER_MODEL = None

SESSION_TYPE = 'cookie'
SESSION_EXPIRES = True
SESSION_AUTO = False
SESSION_HTTP_ONLY = True
SESSION_SECURE = True
SESSION_COOKIE_DOMAIN = None

USE_CSRF = True
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = 'xsrftoken'
CSRF_COOKIE_AGE = 60 * 60 * 24 * 365
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_HEADER_NAME = 'X-XSRFTOKEN'
CSRF_TRUSTED_ORIGINS = []
