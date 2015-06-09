from manoseimas.settings.base import *  # noqa

from debug_toolbar.settings import PANELS_DEFAULTS


DEBUG = True

INTERNAL_IPS = (
    '127.0.0.1',
)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BUILDOUT_DIR, 'var', 'mail')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_PANELS = PANELS_DEFAULTS + [
    'sboard.debugtoolbar.NodeDebugPanel',
]

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEST_RUNNER = 'sboard.testrunner.SboardTestSuiteRunner'

AUTHENTICATION_BACKENDS += (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS += (
    'debug_toolbar',
)

DATABASES['default']['NAME'] = 'manoseimas'
