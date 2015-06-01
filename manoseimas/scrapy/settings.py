# Initialize django
import os.path
import exportrecipe
BUILDOUT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')
)
config = exportrecipe.load(os.path.join(BUILDOUT_DIR, 'settings.json'))
os.environ['DJANGO_SETTINGS_MODULE'] = config.django_settings
import django
django.setup()


BOT_NAME = 'manoseimas.lt'

SPIDER_MODULES = ['manoseimas.scrapy.spiders']
NEWSPIDER_MODULE = 'manoseimas.scrapy.spiders'
DEFAULT_ITEM_CLASS = 'manoseimas.scrapy.items.Person'
USER_AGENT = '%s/1.1' % (BOT_NAME)

LOG_ENABLED = True
LOG_LEVEL = 'WARNING'  # CRITICAL, ERROR, WARNING, INFO, DEBUG
# LOG_FILE = os.path.join(settings.BUILDOUT_DIR, 'var', 'log', 'scrapy.log')

ITEM_PIPELINES = [
    # 'manoseimas.scrapy.pipelines.ManoseimasPipeline',
    'manoseimas.scrapy.pipelines.ManoSeimasModelPersistPipeline',
]

DOWNLOADER_MIDDLEWARES = {
    'manoseimas.scrapy.downloadermiddleware.NoCacheInitialURLMiddleware': 1
}

HTTPCACHE_ENABLED = True
HTTPCACHE_POLICY = 'manoseimas.scrapy.httpcache.NoCacheFlagPolicy'
HTTPCACHE_STORAGE = 'scrapy.contrib.httpcache.LeveldbCacheStorage'
HTTPCACHE_DIR = '/tmp/manoseimas_httpcache'

COUCHDB_URL = 'http://127.0.0.1:5984'

COUCHDB_DATABASES = (
    ('legalact', COUCHDB_URL, 'legalacts',),
    ('question', COUCHDB_URL, 'sittings',),
    ('voting', COUCHDB_URL, 'sittings',),
    ('person', COUCHDB_URL, 'mps',),
)
