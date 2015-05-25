# import os.path
# from django.core.management import setup_environ
# import manoseimas.settings
# setup_environ(manoseimas.settings)
# from django.conf import settings


BOT_NAME = 'manoseimas.lt'

SPIDER_MODULES = ['manoseimas.scrapy.spiders']
NEWSPIDER_MODULE = 'manoseimas.scrapy.spiders'
DEFAULT_ITEM_CLASS = 'manoseimas.scrapy.items.Person'
USER_AGENT = '%s/1.1' % (BOT_NAME)

LOG_ENABLED = True
LOG_LEVEL = 'WARNING' # CRITICAL, ERROR, WARNING, INFO, DEBUG
# LOG_FILE = os.path.join(settings.BUILDOUT_DIR, 'var', 'log', 'scrapy.log')

# HTTPCACHE_ENABLED = True
# HTTPCACHE_DIR = os.path.join(settings.BUILDOUT_DIR, 'var', 'httpcache')

ITEM_PIPELINES = [
    'manoseimas.scrapy.pipelines.ManoseimasPipeline',
]

COUCHDB_DATABASES = (
    ('legalact', 'http://127.0.0.1:5984', 'legalacts',),
    ('question', 'http://127.0.0.1:5984', 'sittings',),
    ('voting', 'http://127.0.0.1:5984', 'sittings',),
    ('person', 'http://127.0.0.1:5984', 'mps',),
)
