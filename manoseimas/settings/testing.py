from manoseimas.settings.base import *  # noqa

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

WEBPACK_LOADER.update({
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BUILDOUT_DIR, 'webpack-stats.json'),
    }
})

WEBPACK_COMMAND = ['npm', 'run', 'build:hot-reload']
