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
NOSE_ARGS = [
    '-w%s' % PROJECT_DIR,    # working dir
    '-w.',                   # project dir (relative to working dir)
    '-w../parts/django-sboard/sboard',
    '--all-modules',         # search tests in all modules
    '--with-doctest',        # search doctests
    '--no-path-adjustment',  # do no adjust sys.path, it is already do by
                             # zc.buildout
    '--nocapture',           # do no capture output
    '--id-file=%s' % os.path.join(BUILDOUT_DIR, 'var', 'noseids'),
                             # store node id file in var direcotory
]

AUTHENTICATION_BACKENDS += (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS += (
    'django.contrib.admin',
    'debug_toolbar',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'db.sqlite3'),
    }
}
