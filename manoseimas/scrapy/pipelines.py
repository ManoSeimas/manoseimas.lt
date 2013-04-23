import datetime

from couchdbkit import ResourceNotFound
from couchdbkit import Server

from manoseimas.scrapy.settings import COUCHDB_DATABASES

_dbs = {}
_servers = {}
_docs = {}


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
        set_db_from_settings(COUCHDB_DATABASES, item_name)
    return _dbs[item_name]

def get_doc(db, _id, cache=True):
    global _docs
    if cache and _id in _docs:
        return _docs[_id]

    try:
        return db.get(_id)
    except ResourceNotFound:
        return None

def store_doc(db, doc):
    attachments = doc.pop('_attachments', [])
    db.save_doc(doc)
    _docs[doc['_id']] = doc
    print "pipline stored doc %s" % doc['_id']

    for name, content, content_type in attachments:
        db.put_attachment(doc, content, name, content_type)


def is_latest_version(item, doc):
    item_version = item.get('source', {}).get('version')
    doc_version = doc.get('source', {}).get('version')
    if not item_version or not doc_version:
        return True

    return item_version >= doc_version


class ManoseimasPipeline(object):

    def process_item(self, item, spider):
        if '_id' not in item or not item['_id']:
            raise Exception('Missing doc _id. Doc: %s' % item)

        item_name = item.__class__.__name__.lower()
        db = get_db(item_name)

        doc = get_doc(db, item['_id'])
        if doc is None:
            doc = dict(item)
            doc['doc_type'] = item_name
        else:
            # Some documents contain source versioning. In those cases,
            # we must ensure we're not clobbering a newer sourced
            # document with an older version.
            if not is_latest_version(item, doc):
                print "Rejecting older version of %s (%d < %d)" % (item['_id'], item['source']['version'], doc['source']['version'])
                return
            
            doc.update(item)

        doc['updated'] = datetime.datetime.now().isoformat()
        store_doc(db, doc)

        return item
