from collections import defaultdict

from couchdb.design import ViewDefinition
import couchdb


DATABASES = None

VIEWS = (

('legalact', 'by_update_time',
'''function (doc) {
    if (doc.updated) {
        emit(doc.updated, null)
    }
}''', None),

('legalact', 'by_name',
'''function (doc) {
    if (doc.name) {
        emit(doc.name, null)
    }
}''', None),


('voting', 'votes_with_documents',
'''function (doc) {
    if (doc.doc_type == 'voting' && doc.documents) {
        emit(doc._id, null);
    }
}''', None),

)

def get_databases(dbs):
    global DATABASES
    if DATABASES is None:
        servers = {}
        DATABASES = {}
        for item, server, db in dbs:
            if server not in servers:
                servers[server] = couchdb.Server(server)
            DATABASES[item] = servers[server][db]
        sync_views(DATABASES, VIEWS)
    return DATABASES


def sync_views(db, views):
    views_to_sync = defaultdict(list)
    for item, name, mapfn, reducefn in views:
        view = ViewDefinition('scrapy', name, mapfn, reducefn)
        views_to_sync[item].append(view)
    for item, views in views_to_sync.items():
        ViewDefinition.sync_many(db[item], views)
