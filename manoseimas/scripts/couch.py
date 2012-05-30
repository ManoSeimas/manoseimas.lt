# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.

import argparse

from couchdbkit import Server

from django.core.management import setup_environ
from manoseimas import settings
setup_environ(settings)

from django.conf import settings


def replicate(args):
    server = Server(settings.COUCHDB_SERVER)
    server.replicate(args.source, args.target)


def shell(args):
    import IPython
    shell = IPython.Shell.IPShellEmbed()
    shell()


def deletesittings(args):
    server = Server(settings.COUCHDB_SERVER)
    db = server['nodes']
    total = db.view('votings/by_source_id', limit=1).total_rows
    counter = 0
    pages = 0
    while pages < total:
        for doc in db.view('votings/by_source_id', include_docs=True, limit=1000):
            counter += 1
            if doc['doc']['doc_type'] == 'Voting':
                print('del %s / %s' % (counter, total))
                del db[doc['doc']['_id']]
        pages += 100


def _list_nodes(view, db='nodes', page=50, **params):
    server = Server(settings.COUCHDB_SERVER)
    db = server[db]

    params['include_docs'] = params.get('include_docs', True)

    counter = 0
    while counter == 0:
        counter = 1
        params['limit'] = page + 1
        for doc in db.view(view, **params):
            counter += 1
            if counter >= page:
                counter = 0
                params['startkey'] = doc['key']
                params['startkey_docid'] = doc['id']
            else:
                yield doc['doc']


def listmpprofiles(args):
    params = dict(
        startkey=['MPProfile', u'\ufff0'],
        endkey=['MPProfile'],
        descending=True
    )
    for doc in _list_nodes('sboard/by_type', **params):
        print('[ %s ]: %s' % (doc['_id'], doc.get('title')))


def listgroups(args):
    groups = [
        'Party',
        'Fraction',
        'Committee',
        'Commission',
        'Parliament',
        'ParliamentaryGroup',
    ]
    for group in groups:
        print(group)
        params = dict(
            startkey=[group, u'\ufff0'],
            endkey=[group],
            descending=True
        )
        for doc in _list_nodes('sboard/by_type', **params):
            print(u'[ %s ]: %s' % (doc['_id'], doc.get('title')))


def deletempgroups(args):
    server = Server(settings.COUCHDB_SERVER)
    db = server['nodes']

    print('Deleting groups and MP profiles.')
    groups = [
        'Party',
        'Fraction',
        'Committee',
        'Commission',
        'Parliament',
        'ParliamentaryGroup',
    ]
    for group in groups:
        print(group)
        params = dict(
            startkey=[group, u'\ufff0'],
            endkey=[group],
            descending=True
        )
        for doc in _list_nodes('sboard/by_type', **params):
            print('DEL: [ %s ]: %s' % (doc['_id'], doc.get('title')))
            del db[doc['_id']]

    db = server['mps']
    print('Cleaning mps database.')
    for doc in _list_nodes('_all_docs', db='mps'):
        print('CLEAN: [ %s ]: %s %s' % (doc['_id'], doc.get('first_name'),
                                        doc.get('last_name')))
        for group in range(len(doc.get('groups', []))):
            if 'group_node_id' in doc['groups'][group]:
                doc['groups'][group]['group_node_id'] = None
            if 'membership_node_id' in doc['groups'][group]:
                doc['groups'][group]['membership_node_id'] = None
        db.save_doc(doc)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # replicate
    p = subparsers.add_parser('replicate')
    p.add_argument('source')
    p.add_argument('target')
    p.set_defaults(func=replicate)

    # shell
    p = subparsers.add_parser('shell')
    p.set_defaults(func=shell)

    # deletesittings
    p = subparsers.add_parser('deletesittings')
    p.set_defaults(func=deletesittings)

    # listmpprofiles
    p = subparsers.add_parser('listmpprofiles')
    p.set_defaults(func=listmpprofiles)

    # listgroups
    p = subparsers.add_parser('listgroups')
    p.set_defaults(func=listgroups)

    # deletempgroups
    p = subparsers.add_parser('deletempgroups')
    p.set_defaults(func=deletempgroups)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
