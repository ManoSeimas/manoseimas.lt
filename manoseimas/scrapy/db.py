import datetime

from couchdbkit import ResourceNotFound
from couchdbkit import Server
from couchdbkit import schema


class DateTimeProperty(schema.DateTimeProperty):
    def to_python(self, value):
        if isinstance(value, basestring):
            try:
                value = value.split('.', 1)[0] # strip out microseconds
                value = value[0:19] # remove timezone
                strptime = datetime.datetime.strptime
                if 'T' in value:
                    value = strptime(value, '%Y-%m-%dT%H:%M:%S')
                else:
                    value = strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError, e:
                raise ValueError('Invalid ISO date/time %r [%s]' %
                        (value, str(e)))
        return value

class Source(schema.DocumentSchema):
    id = schema.IntegerProperty()
    url = schema.StringProperty()

class Session(schema.DocumentSchema):
    id = schema.IntegerProperty()
    number = schema.IntegerProperty()
    fakt_pos_id = schema.IntegerProperty()
    type = schema.StringProperty()
    date = DateTimeProperty()


class RawVoting(schema.Document):
    datetime = DateTimeProperty()
    question = schema.StringProperty()
    total_votes = schema.IntegerProperty()
    vote_abstain = schema.IntegerProperty()
    vote_aye = schema.IntegerProperty()
    vote_no = schema.IntegerProperty()
    source = schema.SchemaProperty(Source())

class RawQuestion(schema.Document):
    updated = DateTimeProperty()
    session = schema.SchemaProperty(Session())
    source = schema.SchemaProperty(Source())


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
        from manoseimas.scrapy.settings import COUCHDB_DATABASES
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

    for name, content, content_type in attachments:
        db.put_attachment(doc, content, name, content_type)


def get_voting(_id, cache=True):
    db = get_db('voting')
    return get_doc(db, _id, cache)

def get_question(_id, cache=True):
    db = get_db('question')
    return get_doc(db, _id, cache)


def get_sequential_votings(include_docs=True, descending=False, limit=None, skip=0):
    params = dict(
        include_docs = include_docs,
        limit = limit,
        classes = dict(voting=RawVoting),
    )

    RawVoting.set_db(get_db('voting'))
    return list(RawVoting.view('scrapy/sequential_votings', **params))


