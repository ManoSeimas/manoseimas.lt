import os.path

from django.core.management import setup_environ
from manoseimas import settings
setup_environ(settings)

from django.conf import settings


BOT_NAME = 'manoseimas.lt'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['manoseimas.scrapy.spiders']
NEWSPIDER_MODULE = 'manoseimas.scrapy.spiders'
DEFAULT_ITEM_CLASS = 'manoseimas.scrapy.items.Person'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#LOG_LEVEL = 'WARNING'
#LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(settings.BUILDOUT_DIR, 'var', 'scrapy.log')

#HTTPCACHE_ENABLED = True
#HTTPCACHE_DIR = os.path.join(settings.BUILDOUT_DIR, 'var', 'httpcache')

ITEM_PIPELINES = [
    'manoseimas.scrapy.pipelines.ManoseimasPipeline',
]

COUCHDB_DATABASES = (
    ('legalact', 'http://127.0.0.1:5984/', 'legal_acts',),
    ('question', 'http://127.0.0.1:5984/', 'sittings',),
    ('voting', 'http://127.0.0.1:5984/', 'sittings',),
)
