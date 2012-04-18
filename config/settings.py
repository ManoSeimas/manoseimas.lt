#encoding: utf-8
# coding: utf-8

# $NOTE

import os

PROJECT_DIR = os.path.realpath(os.path.dirname(__file__))
BUILDOUT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

#if $SASS
# Make external tools like SASS and Compass available in PATH.
path = os.environ['PATH'].split(':')
path.append(os.path.join(BUILDOUT_DIR, 'bin'),)
os.environ['PATH'] = ':'.join(path)


s = {
    'PREFIX': os.path.join(BUILDOUT_DIR, 'parts', 'rubygems'),
    'RUBYLIB': os.environ.get('RUBYLIB', ''),
}
os.environ['GEM_HOME'] = '%(PREFIX)s/lib/ruby/gems/1.8' % s
os.environ['RUBYLIB'] = ':'.join([
    '%(RUBYLIB)s', '%(PREFIX)s/lib', '%(PREFIX)s/lib/ruby',
    '%(PREFIX)s/lib/site_ruby/1.8',]) % s
#end if


ugettext = lambda s: s

#if $DEVELOPMENT
DEBUG = True
#else
DEBUG = False
#end if
TEMPLATE_DEBUG = DEBUG
MEDIA_DEV_MODE = DEBUG
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
MEDIAGENERATOR_DIR = os.path.join(BUILDOUT_DIR, 'var', 'mediagenerator')
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(BUILDOUT_DIR, 'parts', 'flot'),
    #if $TWITTER_BOOTSTRAP
    os.path.join(BUILDOUT_DIR, 'parts', 'twitter-bootstrap'),
    #end if
    MEDIAGENERATOR_DIR,
)

DEV_MEDIA_URL = '/mediagenerator/'
PRODUCTION_MEDIA_URL = '/static/'

GENERATED_MEDIA_DIR = os.path.join(BUILDOUT_DIR, 'var', 'www', 'static')
GENERATED_MEDIA_NAMES_FILE = os.path.join(MEDIAGENERATOR_DIR,
                                          '_generated_media_names.py')
#if $SASS
IMPORTED_SASS_FRAMEWORKS_DIR = os.path.join(BUILDOUT_DIR, 'var',
                                            'sass-frameworks')
#end if

MEDIAGENERATOR_DIR = os.path.join(PROJECT_DIR, 'mediagenerator')

GLOBAL_MEDIA_DIRS = (
    MEDIAGENERATOR_DIR,
    os.path.join(BUILDOUT_DIR, 'parts', 'modernizr'),
    #if $JQUERY_VERSION
    os.path.join(BUILDOUT_DIR, 'parts', 'jquery'),
    #end if
    #if $TWITTER_BOOTSTRAP
    os.path.join(BUILDOUT_DIR, 'parts', 'twitter-bootstrap'),
    #end if
    os.path.join(BUILDOUT_DIR, 'parts', 'flot'),
    #if $SASS
    IMPORTED_SASS_FRAMEWORKS_DIR,
    #end if
)

MEDIA_BUNDLES = (
    ('screen.css',
        #if $TWITTER_BOOTSTRAP
        'css/bootstrap.css',
        #end if
        #if $SASS
        'css/screen.sass',
        #else
        'css/screen.css',
        #end if
    ),
    ('modernizr.js',
        'js/modernizr.js',
    ),
    ('scripts.js',
        'js/jquery.js',
        #if $TWITTER_BOOTSTRAP
        # FIXME: boostra.js (parts/twitter-bootstrap/js/bootstrap.js) file does
        # not have anding ';' and breaks other scripts when joining to one
        # file.
        'js/bootstrap.js',
        #end if
        'js/flot/jquery.flot.js',
        'js/flot/jquery.flot.pie.js',
        'js/scripts.js',
    ),
)

BASE_ROOT_MEDIA_FILTERS = {
    '*': 'mediagenerator.filters.concat.Concat',
    'css': '${PROJECT_NAME}.mediagenerator_filters.CSSURL',
}

# This setting works in combination with::
#
#    'css': '${PROJECT_NAME}.mediagenerator_filters.CSSURL',
#
# filter.
REWRITE_CSS_URLS_RELATIVE_TO_SOURCE = False


#if $SASS
SASS_FRAMEWORKS = (
    'compass',
)
#end if

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

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

if MEDIA_DEV_MODE:
    MIDDLEWARE_CLASSES = (('mediagenerator.middleware.MediaMiddleware',) +
                          MIDDLEWARE_CLASSES)

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
    'mediagenerator',
    'social_auth',
    'sorl.thumbnail',
    'couchdbkit.ext.django',
    'commonutils',

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

    'manoseimas.search',
    'manoseimas.legislation',
    'manoseimas.categories',
    'manoseimas.votings',
    'manoseimas.policy',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
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

COUCHDB_SERVER = '$COUCHDB_URL'
COUCHDB_DATABASES = (
    ('sboard', '$COUCHDB_URL/nodes'),
    ('manoseimas.legal_acts', '$COUCHDB_URL/legal_acts'),
    ('manoseimas.categories', '$COUCHDB_URL/nodes'),
    ('manoseimas.legislation', '$COUCHDB_URL/nodes'),
    ('manoseimas.drafts', '$COUCHDB_URL/legal_acts'),
    ('manoseimas.people', '$COUCHDB_URL/people'),
    ('manoseimas.sittings', '$COUCHDB_URL/sittings'),
    ('manoseimas.votings', '$COUCHDB_URL/nodes'),
    ('manoseimas.policy', '$COUCHDB_URL/nodes'),
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

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--failed', '--stop', '--with-doctest',
             '--where', 'manoseimas']
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
    'sboard.nodes.SearchView',
)
