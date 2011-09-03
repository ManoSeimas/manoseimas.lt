from annoying.decorators import render_to

from mscouch.document import Document

import couchdb.design
couch = couchdb.Server('http://127.0.0.1:5984/')
db = couch['manoseimas']

# temporary sync
couchdb.design.ViewDefinition.sync_many(db, [
        Document.by_number,
    ])


@render_to('manoseimas/legislation/index.html')
def index(request):
    return {
        'documents': Document.by_number(db, limit=10),
    }
