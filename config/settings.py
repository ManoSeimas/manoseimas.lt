#encoding: utf-8
# coding: utf-8

# $NOTE

import os

PROJECT_DIR = os.path.realpath(os.path.dirname(__file__))
BUILDOUT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))


ugettext = lambda s: s

#if $DEVELOPMENT
DEBUG = True
#else
DEBUG = False
#end if
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

ADMINS = (
    #if $PRODUCTION
    ('Server Admin', '$SERVER_ADMIN'),
    #end if
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        #if $USE_SQLITE or $DEVELOPMENT
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'db'),
        #else
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'init_command': 'SET storage_engine=INNODB',
            'read_default_file': os.path.join(BUILDOUT_DIR, 'var', 'etc',
                                              'my.cnf'),
        },
        #end if
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Vilnius'

LANGUAGES = (
    #for $lang in $LANGUAGES
    ('$lang', ugettext(u'$LANG_NAMES[$lang]')),
    #end for
)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = '$LANGUAGE_CODE'

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
    #if $JQUERY_VERSION
    os.path.join(BUILDOUT_DIR, 'parts', 'jquery'),
    #end if
    #if $TWITTER_BOOTSTRAP
    os.path.join(BUILDOUT_DIR, 'parts', 'twitter-bootstrap'),
    #end if
    os.path.join(BUILDOUT_DIR, 'parts', 'history.js'),
)

#if $DJANGO_PIPELINE

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
            #if $TWITTER_BOOTSTRAP
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
            #end if
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
    #if $LESS
    'pipeline.compilers.less.LessCompiler',
    #end if
)
#if $LESS
LESS_PATH = ':'.join([
    os.path.join(PROJECT_DIR, 'manoseimas', 'static', 'css'),
    os.path.join(BUILDOUT_DIR, 'parts', 'twitter-bootstrap', 'less'),
])
PIPELINE_LESS_BINARY = os.path.join(BUILDOUT_DIR, 'bin', 'lessc')
PIPELINE_LESS_ARGUMENTS = '--compress --include-path=%s' % LESS_PATH
#end if

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

#end if

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$SECRET_KEY'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #if $DEVELOPMENT
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_pdb.middleware.PdbMiddleware',
    #end if
)

ROOT_URLCONF = '${PROJECT_NAME}.urls'

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
    'django.core.context_processors.request',
    '${PROJECT_NAME}.context_processors.settings_for_context',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'south',
    'social_auth',
    'sorl.thumbnail',
    'couchdbkit.ext.django',
    #if $DJANGO_PIPELINE
    'pipeline',
    #end if

    'sboard',
    'sboard.profiles',
    'sboard.categories',

    #if $DEVELOPMENT
    'debug_toolbar',
    'django_extensions',
    'test_utils',
    'django_pdb',
    'django_nose',
    #end if

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
        'south': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
    }
}

PUBLIC_COUCHDB_SERVER = '$COUCHDB_SERVER_NAME'

COUCHDB_SERVER = '$COUCHDB_URL'
COUCHDB_DATABASES = (
    ('sboard', '$COUCHDB_URL/nodes'),
    ('sboard.profiles', '$COUCHDB_URL/nodes'),

    # XXX: do some thing, that adding these settings should not be necessary.
    ('manoseimas.compat', '$COUCHDB_URL/nodes'),
    ('manoseimas.legislation', '$COUCHDB_URL/nodes'),
    ('manoseimas.mps', '$COUCHDB_URL/nodes'),
    ('manoseimas.solutions', '$COUCHDB_URL/nodes'),
    ('manoseimas.votings', '$COUCHDB_URL/nodes'),
)

ELASTICSEARCH_SERVERS = (
    '127.0.0.1:9200',
)

#if $DEVELOPMENT
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

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    'sboard.debugtoolbar.NodeDebugPanel',
)

TEST_RUNNER = 'sboard.testrunner.SboardTestSuiteRunner'
NOSE_ARGS = [
    '-w${PROJECT_NAME}',     # working dir
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

#else
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
#end if


JQUERY_VERSION = '$JQUERY_VERSION'

PROTOCOL = 'http'
DEFAULT_FROM_EMAIL = '$SERVER_ADMIN'

AUTH_PROFILE_MODULE = 'profiles.Profile'

AUTHENTICATION_BACKENDS = (
    #'social_auth.backends.twitter.TwitterBackend',
    #if $FACEBOOK_APP_ID
    'social_auth.backends.facebook.FacebookBackend',
    #end if
    #'social_auth.backends.google.GoogleOAuthBackend',
    #'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    #'social_auth.backends.yahoo.YahooBackend',
    #'social_auth.backends.contrib.linkedin.LinkedinBackend',
    #'social_auth.backends.contrib.livejournal.LiveJournalBackend',
    #'social_auth.backends.contrib.orkut.OrkutBackend',
    #'social_auth.backends.contrib.foursquare.FoursquareBackend',
    #'social_auth.backends.contrib.github.GithubBackend',
    #'social_auth.backends.contrib.dropbox.DropboxBackend',
    #'social_auth.backends.contrib.flickr.FlickrBackend',
    'social_auth.backends.OpenIDBackend',
    #'django.contrib.auth.backends.ModelBackend',
)

FACEBOOK_APP_ID = '$FACEBOOK_APP_ID'
FACEBOOK_API_SECRET = '$FACEBOOK_API_SECRET'

GOOGLE_ANALYTICS_KEY = '$GOOGLE_ANALYTICS_KEY'

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
