import datetime

from couchdbkit import ResourceNotFound
from couchdbkit import Server

from scrapy.conf import settings

_dbs = {}
_servers = {}


def set_db(item_name, server_name, db_name, cache=True):
    global _servers, _dbs
    if not cache or server_name not in _servers:
        server = _servers[server_name] = Server(server_name)
    else:
        server = _servers[server_name]
    db = _dbs[item_name] = server.get_or_create_db(db_name)
    return db


def set_db_from_settings(settings, item_name, cache=True):
    for item, server_name, db_name in settings:
        if item == item_name:
            return set_db(item_name, server_name, db_name, cache)


def get_db(item_name, cache=True):
    global _servers, _dbs
    if not cache or item_name not in _dbs:
        set_db_from_settings(settings['COUCHDB_DATABASES'], item_name)
    return _dbs[item_name]


class ManoseimasPipeline(object):
    def store_item(self, item_name, doc, item):
        db = get_db(item_name)
        attachments = doc.pop('_attachments', [])
        db.save_doc(doc)

        for name, content, content_type in attachments:
            db.put_attachment(doc, content, name, content_type)

    def get_doc(self, item_name, item):
        db = get_db(item_name)
        try:
            return db.get(item['_id'])
        except ResourceNotFound:
            return None

    def process_item(self, item, spider):
        if '_id' not in item or not item['_id']:
            raise Exception('Missing doc _id. Doc: %s' % item)

        item_name = item.__class__.__name__.lower()

        doc = self.get_doc(item_name, item)
        if doc is None:
            doc = dict(item)
            doc['doc_type'] = item_name
            doc['updated'] = datetime.datetime.now().isoformat()
        else:
            doc.update(item)
            doc['updated'] = datetime.datetime.now().isoformat()

        self.store_item(item_name, doc, item)

        return item
