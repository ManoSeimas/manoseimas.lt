from manoseimas.settings.base import *  # noqa
from manoseimas.settings.development import *  # noqa

BUILDOUT_PARTS_DIR = '/home/vagrant/manoseimas/parts'

INTERNAL_IPS = (
    '127.0.0.1',
    '10.0.2.2',  # Vagrant host IP in default config
)


LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
    os.path.join(BUILDOUT_PARTS_DIR, 'django-sboard/sboard/locale'),
)


STATICFILES_DIRS = (
    os.path.join(BUILDOUT_PARTS_DIR, 'flot'),
    os.path.join(BUILDOUT_PARTS_DIR, 'modernizr'),
    os.path.join(BUILDOUT_PARTS_DIR, 'jquery'),
    os.path.join(BUILDOUT_PARTS_DIR, 'history.js'),
    os.path.join(BUILDOUT_PARTS_DIR, 'bootstrap'),
    os.path.join(BUILDOUT_PARTS_DIR,
                 'bootstrap-sass', 'vendor', 'assets', 'stylesheets'),
    os.path.join(PROJECT_DIR, 'widget', 'frontend', 'build'),
)
