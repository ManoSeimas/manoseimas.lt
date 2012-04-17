import os.path

PROJECT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
# FIXME:sirex: wrong dir...
BUILDOUT_DIR = os.path.abspath(os.path.join(PROJECT_DIR, '..'))

BOT_NAME = 'manoseimas'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['manoseimas.spiders']
NEWSPIDER_MODULE = 'manoseimas.spiders'
DEFAULT_ITEM_CLASS = 'manoseimas.items.Person'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#LOG_LEVEL = 'WARNING'
#LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(PROJECT_DIR, 'crawl.log')

#HTTPCACHE_ENABLED = True
#HTTPCACHE_DIR = os.path.join(BUILDOUT_DIR, 'httpcache')

ITEM_PIPELINES = [
    'manoseimas.pipelines.ManoseimasPipeline',
]

COUCHDB_DATABASES = (
    ('legalact', 'http://127.0.0.1:5984/', 'legal_acts',),
    ('question', 'http://127.0.0.1:5984/', 'sittings',),
    ('voting', 'http://127.0.0.1:5984/', 'sittings',),
)
