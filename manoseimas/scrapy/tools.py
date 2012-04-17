# coding: utf-8

from couchdb.http import ResourceNotFound

from scrapy.conf import settings

from manoseimas.scrapy.couchdb_util import get_databases

db = get_databases(settings['COUCHDB_DATABASES'])


def fixdocs():
    for doc in db['legalact'].view('_all_docs', include_docs=True):
        doc = doc.doc
        for old, new in [
                    ('amended_documents', 'amends'),
                    ('adopted_documents', 'adopts'),
                    ('defines_applicability', 'defines_applicability'),
                    ('defines_validity', 'defines_validity'),
                ]:
            if old in doc:
                if 'relations' not in doc:
                    doc['relations'] = {}
                doc['relations'][new] = doc[old][:]
                del doc[old]
                db['legalact'][doc['_id']] = doc
                print('Fixed: %s' % doc.get('_id'))


def list_docs():
    filename = '/tmp/law.txt'
    with open(filename, 'w') as f:
        for doc in db['legalact'].view('legislation/by_name', include_docs=True):
            doc = doc.doc
            if 'name' in doc and 'ratifikavimo' in doc['name'].lower():
                try:
                    f.write("'%s',\n" % doc['source']['url'])
                except KeyError:
                    pass
    print('Done: %s' % filename)


def docs_with_space_in_key():
    for doc in db['legalact'].view('_all_docs', startkey=' ', endkey=' Z',
                       include_docs=True):
        print(doc)

def type_to_kind():
    for doc in db['legalact'].view('_all_docs', include_docs=True):
        doc = doc.doc
        if 'type' in doc:
            doc['kind'] = doc['type']

            if (doc['type'] in (u'įstatymas', u'konstitucija') and
                not doc.get('relations')):
                doc['type'] = u'įstatymas'

            elif doc['type'] == u'įstatymas':
                doc['type'] = u'įstatymo pataisa'

            db['legalact'][doc['_id']] = doc


def link_draft_with_law():
    for row in db['legalact'].view('_all_docs', include_docs=True, skip=90, limit=10):
        doc = row.doc
        name = doc['name'].split(u' įstatymo ', 2)[0]
        if name:
            name = name + u' įstatymas'
            rs = db['legalact'].view('legislation/by_name', key=name, include_docs=True)
            if len(rs) > 0:
                if 'relations' not in doc:
                    doc['relations'] = {}
                doc['relations']['law'] = [rs.rows[0]['id']]
                db['legalact'][doc['_id']] = doc


def _get_parents(db, pkey, level=0):
    parents = set([pkey])

    if level > 7:
        return parents

    try:
        pdoc = db[pkey]
    except ResourceNotFound:
        pass
    else:
        if 'relations' in pdoc:
            for relkey in ('law', 'new_draft_version', 'adopts', 'amends'):
                if relkey in pdoc['relations']:
                    for key in pdoc['relations'][relkey]:
                        parents.update(_get_parents(db, key, level+1))
    return parents


def votings_get_parents():
    view = db['voting'].view('scrapy/votes_with_documents', include_docs=True)
    for row in view:
        doc = row.doc

        parents = set()
        for pkey in doc['documents']:
            parents.update(_get_parents(db['legalact'], pkey))

        doc['parents'] = list(parents)

        db['voting'].save(doc)



tool = votings_get_parents
