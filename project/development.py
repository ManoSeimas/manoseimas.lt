from project.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = (
    '127.0.0.1',
)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BUILDOUT_DIR, 'var', 'mail')

CACHE_BACKEND = "dummy://"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'development.db'),
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
    'test_utils',
)
