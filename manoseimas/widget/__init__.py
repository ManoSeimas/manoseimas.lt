from django.db.models import signals


def syncdb(app, created_models, verbosity=2, **kwargs):
    from manoseimas.widget.couchdb import syncdb
    syncdb(app, verbosity=verbosity)


signals.post_syncdb.connect(syncdb)
