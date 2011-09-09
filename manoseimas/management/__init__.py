import os

from django.conf import settings
from django.db.models.signals import post_syncdb

from couchdbkit.ext.django.loading import get_db
from couchdbkit.loaders import FileSystemDocsLoader

import manoseimas


def sync_plugins(sender, verbosity, **kwargs):
    couchdesign = os.path.join(settings.PROJECT_DIR, 'couchdesign')
    loader = FileSystemDocsLoader(couchdesign)
    loader.sync(get_db('manoseimas'), verbose=verbosity)
post_syncdb.connect(sync_plugins, sender=manoseimas.models)
