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

ADMINS = (
    #if $PRODUCTION
    ('Server Admin', '$SERVER_ADMIN'),
    #end if
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        #if $DEVELOPMENT
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BUILDOUT_DIR, 'var', 'development.db'),
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
  ('lt', ugettext(u'Lietuvių')),
)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'lt'

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

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BUILDOUT_DIR, 'var', 'www', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BUILDOUT_DIR, 'manoseimas', 'static'),
    os.path.join(BUILDOUT_DIR, 'var', 'sass'),
    os.path.join(BUILDOUT_DIR, 'parts', 'flot'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8m86q=ycpwma&n1f0t-l)y(i&lx*aon=%!(uuv985a-t+a_bfw'

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
    #if $DEVELOPMENT
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #end if
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
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'couchdbkit.ext.django',
    'registration',

    #if $DEVELOPMENT
    'debug_toolbar',
    'django_extensions',
    'test_utils',
    #end if

    'manoseimas.search',
    'manoseimas.legislation',
    'manoseimas.categories',
    'manoseimas.votings',
    'manoseimas.accounts',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

COUCHDB_DATABASES = (
    ('manoseimas.legal_acts', '$COUCHDB_URL/legal_acts'),
    ('manoseimas.categories', '$COUCHDB_URL/categories'),
    ('manoseimas.legislation', '$COUCHDB_URL/legal_acts'),
    ('manoseimas.drafts', '$COUCHDB_URL/legal_acts'),
    ('manoseimas.people', '$COUCHDB_URL/people'),
    ('manoseimas.sittings', '$COUCHDB_URL/sittings'),
    ('manoseimas.votings', '$COUCHDB_URL/sittings'),
    ('manoseimas.profiles', '$COUCHDB_URL/profiles'),
)

#if $DEVELOPMENT
INTERNAL_IPS = (
    '127.0.0.1',
)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BUILDOUT_DIR, 'var', 'mail')

CACHE_BACKEND = "dummy://"

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
#end if
