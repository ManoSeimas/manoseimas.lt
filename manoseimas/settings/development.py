from manoseimas.settings.base import *  # noqa

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

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INSTALLED_APPS += (
    'debug_toolbar',
)

DATABASES['default']['NAME'] = 'manoseimas'

WEBPACK_LOADER.update({
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BUILDOUT_DIR, 'webpack-stats.json'),
    }
})

WEBPACK_COMMAND = ['npm', 'run', 'build:hot-reload']
