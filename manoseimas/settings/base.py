# coding: utf-8

import os.path
import exportrecipe

from django.utils.translation import ugettext_lazy as _


PROJECT_DIR = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
BUILDOUT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

config = exportrecipe.load(os.path.join(BUILDOUT_DIR, 'settings.json'))

DEBUG = False

ADMINS = (
    ('Server Admin', 'manoseimas@doublemarked.com'),
)

MANAGERS = ADMINS

ATOMIC_REQUESTS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            'read_default_file': os.path.expanduser('~/.my.cnf'),
        },
    }
}

TIME_ZONE = 'Europe/Vilnius'

LANGUAGES = (
    ('lt', _('Lithianian')),
)

LANGUAGE_CODE = 'lt'

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
    os.path.join(config.buildout_parts_dir, 'django-sboard/sboard/locale'),
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
    os.path.join(config.buildout_parts_dir, 'modernizr'),
    os.path.join(config.buildout_parts_dir, 'jquery'),
    os.path.join(config.buildout_parts_dir, 'history.js'),
    os.path.join(config.buildout_parts_dir, 'bootstrap'),
    os.path.join(config.buildout_parts_dir, 'bootstrap-sass', 'vendor', 'assets', 'stylesheets'),
    os.path.join(PROJECT_DIR, 'widget', 'frontend', 'build'),
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
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config.secret_key

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'manoseimas.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'manoseimas.context_processors.settings_for_context',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_auth',
    'sorl.thumbnail',
    'couchdbkit.ext.django',
    'compressor',

    'sboard',
    'sboard.profiles',
    'sboard.categories',

    'django_extensions',
    'test_utils',
    'django_nose',

    'manoseimas.legislation',
    'manoseimas.votings',
    'manoseimas.mps',
    'manoseimas.mps_v2',
    'manoseimas.solutions',         # depends on: votings
    'manoseimas.compat',            # depends on: solutions
    'manoseimas',                   # depends on: votings
    'manoseimas.widget',
)


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
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        '': { # wildcard
            'level': 'DEBUG',
            'handlers': ['everything'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db': {
            'handlers': ['null'],
            'level': 'INFO',
            'propagate': True,
        },
        'couchdbkit': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'restkit': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
    }
}

PUBLIC_COUCHDB_SERVER = 'http://couchdb.manoseimas.lt/'

COUCHDB_SERVER = config.couchdb_server
COUCHDB_DATABASES = (
    ('sboard', COUCHDB_SERVER + 'nodes'),
    ('sboard.profiles', COUCHDB_SERVER + 'nodes'),

    # XXX: do some thing, that adding these settings should not be necessary.
    ('manoseimas.compat', COUCHDB_SERVER + 'nodes'),
    ('manoseimas.legislation', COUCHDB_SERVER + 'nodes'),
    ('manoseimas.mps', COUCHDB_SERVER + 'nodes'),
    ('manoseimas.solutions', COUCHDB_SERVER + 'nodes'),
    ('manoseimas.votings', COUCHDB_SERVER + 'nodes'),
)

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

AUTH_PROFILE_MODULE = 'profiles.Profile'

AUTHENTICATION_BACKENDS = (
    # 'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    # 'social_auth.backends.google.GoogleOAuthBackend',
    # 'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    # 'social_auth.backends.yahoo.YahooBackend',
    # 'social_auth.backends.contrib.linkedin.LinkedinBackend',
    # 'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    # 'social_auth.backends.contrib.orkut.OrkutBackend',
    # 'social_auth.backends.contrib.foursquare.FoursquareBackend',
    # 'social_auth.backends.contrib.github.GithubBackend',
    # 'social_auth.backends.contrib.dropbox.DropboxBackend',
    # 'social_auth.backends.contrib.flickr.FlickrBackend',
    'social_auth.backends.OpenIDBackend',
)

FACEBOOK_APP_ID = config.facebook_app_id
FACEBOOK_API_SECRET = config.facebook_api_secret
GOOGLE_ANALYTICS_KEY = config.google_analytics_key

SBOARD_NODES = (
    'sboard.categories.nodes.CategoryNode',
    'manoseimas.legislation.nodes.LawNode',
    'manoseimas.legislation.nodes.LawChangeNode',
    'manoseimas.legislation.nodes.LawProjectNode',
    'manoseimas.votings.nodes.VotingNode',
    'manoseimas.policy.nodes.PolicyNode',
)

SBOARD_SEARCH_HANDLERS = (
    'manoseimas.votings.nodes.search_lrs_url',
    'manoseimas.compat.nodes.CompatSearchView',
)

SBOARD_PAGE_TEMPLATES = (
    ('sboard/page.html', 'Plain page'),
    ('index.html', 'Index page'),
)

RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'footnote_references': 'superscript',
    'math_output': 'MathJax',
}

THUMBNAIL_QUALITY = 100

# This is only for anonymous users and is overriden when a user logs in.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
