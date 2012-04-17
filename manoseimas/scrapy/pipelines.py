import datetime

import couchdb

from scrapy import signals
from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher

from manoseimas.scrapy.couchdb_util import get_databases


class ManoseimasPipeline(object):
    def __init__(self):
        self.db = get_databases(settings['COUCHDB_DATABASES'])
        self.spider_started = datetime.datetime.now().isoformat()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        if hasattr(spider, 'post_process'):
            getattr(spider, 'post_process')(self.db, self.spider_started)

    def process_item(self, item, spider):
        item_name = item.__class__.__name__.lower()
        now = datetime.datetime.now().isoformat()

        doc = self.get_existing(item_name, item)
        if doc:
            changed = False
        else:
            doc = {'doc_type': item_name}
            changed = True

        for key in item.keys():
            if key in ('_attachments',):
                continue

            if isinstance(item[key], datetime.datetime):
                new = item[key].isoformat()
            else:
                new = item[key]

            if not changed and (key not in doc or new != doc[key]):
                changed = True

            doc[key] = new

        if changed:
            doc['updated'] = now
            if '_id' in doc:
                if not doc['_id']:
                    raise Exception(str(doc))
                self.db[item_name][doc['_id']] = doc
            else:
                self.db[item_name].save(doc)

            if '_attachments' in item:
                if '_rev' not in doc:
                    doc = self.db[item_name][doc['_id']]
                for attachment, content in item['_attachments']:
                    self.db[item_name].put_attachment(doc, content, attachment)

        return item

    def get_existing(self, item_name, item):
        try:
            return self.db[item_name][item['_id']]
        except couchdb.http.ResourceNotFound:
            return None
