# couchdbkit won't sync our CouchDB views because there are no document
# schemas registered in manoseimas.widget, so we have to load the views
# ourselves.

import os

from couchdbkit import push
from sboard.models import Node


def syncdb(app, verbosity=2):
    # Fun fact: syncdb will never be called for manoseimas.widget.models,
    # because we don't have any MySQL models here.  Since we want to run
    # exactly once, let's hook up after the main app.
    if app.__name__ != 'manoseimas.models':
        return
    if verbosity >= 1:
        print "sync `manoseimas.widget` in CouchDB"
    db = Node.get_db()
    path = os.path.join(os.path.dirname(__file__), '_design')
    push(path, db, force=True, docid='_design/widget')
