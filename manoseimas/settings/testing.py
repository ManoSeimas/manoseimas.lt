from manoseimas.settings.base import *  # noqa

TEST_RUNNER = 'sboard.testrunner.SboardTestSuiteRunner'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
