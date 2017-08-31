# coding: utf-8

import os
import os.path
import exportrecipe
import platform
import collections

from datetime import datetime as dt
from django.utils.translation import ugettext_lazy as _

DateTimeRange = collections.namedtuple('DateTimeRange', ['since', 'until'])

# Current parliament term
TERM_OF_OFFICE_RANGE = DateTimeRange(dt(2016, 11, 14), dt(2020, 10, 9))

# All parliament terms
PARLIAMENT_TERMS = {
    '2016-2020': DateTimeRange(dt(2016, 11, 14), dt(2020, 10, 9)),
    '2012-2016': DateTimeRange(dt(2012, 10, 14), dt(2016, 10, 9)),
    '2008-2012': DateTimeRange(dt(2008, 10, 12), dt(2012, 10, 14)),
}

DIST = platform.linux_distribution()[:2]

PROJECT_DIR = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
BUILDOUT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

config = exportrecipe.load(os.path.join(BUILDOUT_DIR, 'settings.json'))

DEBUG = False

ALLOWED_HOSTS = ['manoseimas.lt', 'www.manoseimas.lt',
                 'manoseimas-staging.pov.lt',
                 'ms.tinginiai.lt', 'manoseimas.nous.lt', 'localhost']

ADMINS = (
    ('Server Admin', 'sirexas@gmail.com'),
)

MANAGERS = ADMINS

ATOMIC_REQUESTS = True

# if DIST == ('Ubuntu', '16.04') or platform.system() == 'Darwin':
# With MySQL 5.7 the command SET storage_engine=MyISAM won't work.
# http://stackoverflow.com/a/37220446/475477
init_command = 'SET default_storage_engine=INNODB'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'manoseimas',
        'OPTIONS': {
            'init_command': init_command,
            'read_default_file': os.path.expanduser('~/.my.cnf'),
        },
    }
}

TIME_ZONE = 'Europe/Vilnius'

LANGUAGES = (
    ('lt', _('Lithuanian')),
)

LANGUAGE_CODE = 'lt'

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

SITE_ID = 1

# Django-registration settings.
ACCOUNT_ACTIVATION_DAYS = 7

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'www', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'www', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(config.buildout_parts_dir, 'flot'),
    os.path.join(config.buildout_parts_dir, 'jquery'),
    os.path.join(config.buildout_parts_dir, 'history.js'),
    os.path.join(config.buildout_parts_dir, 'bootstrap'),
    os.path.join(config.buildout_parts_dir, 'bootstrap-sass', 'vendor', 'assets', 'stylesheets'),
    os.path.join(PROJECT_DIR, 'widget', 'frontend', 'build'),
    os.path.join(BUILDOUT_DIR, 'build'),
    os.path.join(BUILDOUT_DIR, 'bundles'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Django compressor settings
# http://django-compressor.readthedocs.org/en/latest/settings/

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)

COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/x-scss', 'django_libsass.SassCompiler'),
    ('text/jsx', 'manoseimas.common.jsx.JSXCompiler'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.secret_key


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'manoseimas.context_processors.settings_for_context',
            ],
            'loaders': [
                ('pyjade.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ]
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'manoseimas.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'social.apps.django_app.default',
    'sorl.thumbnail',
    'compressor',
    'haystack',
    'lazysignup',

    'manoseimas',

    'django_extensions',
    'test_utils',
    'django_nose',

    'manoseimas.mps_v2',
    'manoseimas.widget',
    'manoseimas.lobbyists',
    'manoseimas.compatibility_test',
    'manoseimas.flatpages',
    'manoseimas.scrapy',

    'rest_framework',
    'webpack_loader',
    'django_wysiwyg',
    'tinymce',
)

MIGRATION_MODULES = {
    'default': 'manoseimas.migrations.python_social_auth',
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'everything': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': os.path.join(BUILDOUT_DIR, 'var/log/django.log'),
            'backupCount': 2,
            'maxBytes': 1024 * 1024 * 3,
        },
        'error_log': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'verbose',
            'filename': os.path.join(BUILDOUT_DIR, 'var/log/error.log'),
            'backupCount': 2,
            'maxBytes': 1024 * 1024 * 3,
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        '': {  # wildcard
            'level': 'DEBUG',
            'handlers': ['everything'],
        },
        'django.request': {
            'handlers': ['error_log', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

ELASTICSEARCH_SERVERS = (
    '127.0.0.1:9200',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

PROTOCOL = 'http'
DEFAULT_FROM_EMAIL = 'manoseimas@doublemarked.com'

AUTH_USER_MODEL = 'manoseimas.ManoSeimasUser'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.open_id.OpenIdAuth',
    'lazysignup.backends.LazySignupBackend',
)

GOOGLE_ANALYTICS_KEY = config.google_analytics_key

SOCIAL_AUTH_FACEBOOK_KEY = config.facebook_app_id
SOCIAL_AUTH_FACEBOOK_SECRET = config.facebook_api_secret

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config.google_oauth2_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config.google_oauth2_secret

RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'footnote_references': 'superscript',
    'math_output': 'MathJax',
}

THUMBNAIL_QUALITY = 100

# This is only for anonymous users and is overriden when a user logs in.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Django-social-auth does not support JSON serializer.
# See: https://docs.djangoproject.com/en/1.8/topics/http/sessions/#session-serialization
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BUILDOUT_DIR, 'webpack-stats-prod.json'),
    }
}

DJANGO_WYSIWYG_FLAVOR = "tinymce_advanced"

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BUILDOUT_DIR, 'var', 'whoosh_index'),
    },
}

# We have compatibility_test and many similar names ending with _test, so we need a better test discovery.
NOSE_ARGS = ['--match', '^[Tt]est']
