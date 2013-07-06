import datetime

from manoseimas.scrapy.db import get_db, get_doc, store_doc

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
                return
            
            doc.update(item)

        doc['updated'] = datetime.datetime.now().isoformat()
        store_doc(db, doc)

        return item
