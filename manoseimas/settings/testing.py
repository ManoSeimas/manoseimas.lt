from manoseimas.settings.base import *  # noqa

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
