from __future__ import unicode_literals, print_function

import os
import os.path

from couchdbkit import Server
from couchdbkit import push

from manoseimas.scrapy.settings import COUCHDB_URL, BUILDOUT_DIR


def main():
    server = Server(COUCHDB_URL)
    couchdb_dir = os.path.join(BUILDOUT_DIR, 'manoseimas', 'scrapy', 'couchdb')
    for dbname in os.listdir(couchdb_dir):
        print("sync %s..." % dbname)
        db = server.get_or_create_db(dbname)
        path = os.path.join(couchdb_dir, dbname)
        push(path, db, force=True, docid='_design/scrapy')
    print("done.")


if __name__ == '__main__':
    main()
