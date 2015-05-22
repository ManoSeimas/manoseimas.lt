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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            'read_default_file': os.path.join(BUILDOUT_DIR, 'var', 'etc', 'my.cnf'),
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
    os.path.join(BUILDOUT_DIR, 'parts/django-sboard/sboard/locale'),
)

SITE_ID = 1

# Django-registration settings.
ACCOUNT_ACTIVATION_DAYS = 7

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'www', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'www', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(BUILDOUT_DIR, 'parts', 'flot'),
    os.path.join(BUILDOUT_DIR, 'parts', 'modernizr'),
    os.path.join(BUILDOUT_DIR, 'parts', 'jquery'),
    os.path.join(BUILDOUT_DIR, 'parts', 'twitter-bootstrap'),
    os.path.join(BUILDOUT_DIR, 'parts', 'history.js'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_CSS = {
    'styles': {
        'source_filenames': (
          'fonts/open-sans/stylesheet.less',
          'css/styles.less',
        ),
        'output_filename': 'css/styles.css',
        'variant': 'datauri',
    },
}

PIPELINE_JS = {
    'scripts': {
        'source_filenames': (
            'js/jquery.js',
            'js/bootstrap-transition.js',
            'js/bootstrap-alert.js',
            'js/bootstrap-button.js',
            'js/bootstrap-carousel.js',
            'js/bootstrap-collapse.js',
            'js/bootstrap-dropdown.js',
            'js/bootstrap-modal.js',
            'js/bootstrap-tooltip.js',
            'js/bootstrap-popover.js',
            'js/bootstrap-scrollspy.js',
            'js/bootstrap-tab.js',
            'js/bootstrap-typeahead.js',
            'js/bootstrap-affix.js',
            'js/flot/jquery.flot.js',
            'js/flot/jquery.flot.pie.js',
            'js/csrf.js',
            'scripts/uncompressed/history.adapter.jquery.js',
            'scripts/uncompressed/history.js',
            'js/manoSeimas.js',
        ),
        'output_filename': 'js/scripts.min.js',
    },

    'modernizr': {
        'source_filenames': (
            'js/modernizr.js',
        ),
        'output_filename': 'js/modernizr.min.js',
    },
}

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)
LESS_PATH = ':'.join([
    os.path.join(PROJECT_DIR, 'manoseimas', 'static', 'css'),
    os.path.join(BUILDOUT_DIR, 'parts', 'twitter-bootstrap', 'less'),
])
PIPELINE_LESS_BINARY = os.path.join(BUILDOUT_DIR, 'bin', 'lessc')
PIPELINE_LESS_ARGUMENTS = '--compress --include-path=%s' % LESS_PATH

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

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
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'manoseimas.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
)

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
    # 'couchdbkit.ext.django',
    'pipeline',

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

COUCHDB_SERVER = 'http://127.0.0.1:5984/'
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
