# couchdbkit won't sync our CouchDB views because there are no document
# schemas registered in manoseimas.widget, so we have to load the views
# ourselves.

import os

from django.conf import settings
from couchdbkit.ext.django.loading import CouchdbkitHandler
from couchdbkit import push


def syncdb(app, verbosity=2):
    # Fun fact: syncdb will never be called for manoseimas.widget.models,
    # because we don't have any MySQL models here.  Since we want to run
    # exactly once, let's hook up after the main app.
    if app.__name__ != 'manoseimas.models':
        return
    if verbosity >= 1:
        print "sync `manoseimas.widget` in CouchDB"
    # Getting the database is a tricky business: this gets called early
    # during unit test setup, and we don't want to touch the real DB
    # during unit test runs, do we?  At this point settings.COUCHDB_DATABASES
    # has been modified by sboard.testrunner.SboardTestSuiteRunner, but
    # nothing else.
    handler = CouchdbkitHandler(settings.COUCHDB_DATABASES)
    db = handler.get_db('widget')
    path = os.path.join(os.path.dirname(__file__), '_design')
    push(path, db, force=True, docid='_design/widget')
