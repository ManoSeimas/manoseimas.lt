# import os.path
# 
# from django.core.management import setup_environ
# import manoseimas.settings
# setup_environ(manoseimas.settings)
# 
# from django.conf import settings


BOT_NAME = 'manoseimas.lt'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['manoseimas.scrapy.spiders']
NEWSPIDER_MODULE = 'manoseimas.scrapy.spiders'
DEFAULT_ITEM_CLASS = 'manoseimas.scrapy.items.Person'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

LOG_ENABLED = True
LOG_LEVEL = 'WARNING' # CRITICAL, ERROR, WARNING, INFO, DEBUG
# LOG_FILE = os.path.join(settings.BUILDOUT_DIR, 'var', 'log', 'scrapy.log')

# HTTPCACHE_ENABLED = True
# HTTPCACHE_DIR = os.path.join(settings.BUILDOUT_DIR, 'var', 'httpcache')

ITEM_PIPELINES = [
    'manoseimas.scrapy.pipelines.ManoseimasPipeline',
]

COUCHDB_DATABASES = (
    ('legalact', '$COUCHDB_URL', 'legalacts',),
    ('question', '$COUCHDB_URL', 'sittings',),
    ('voting', '$COUCHDB_URL', 'sittings',),
    ('person', '$COUCHDB_URL', 'mps',),
)
