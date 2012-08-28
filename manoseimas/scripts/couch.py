# coding: utf-8

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


class ScriptError(Exception):
    pass


def replicate(args):
    if args.source is None:
        replications = (
            ('http://couchdb.manoseimas.lt/mps', 'mps'),
            ('http://couchdb.manoseimas.lt/nodes', 'nodes'),
            ('http://couchdb.manoseimas.lt/sittings', 'sittings'),
        )
    else:
        if not all(args.source, args.target):
            raise ScriptError('Specify source and target.')
        replications = (
            (args.source, args.target),
        )
    server = Server(settings.COUCHDB_SERVER)
    for source, target in replications:
        print('Replicating: %s -> %s' % (source, target))
        server.replicate(source, target)


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
                db.delete_doc(doc['doc'])
        pages += 100


def _list_nodes(view, db='nodes', page=2, **params):
    server = Server(settings.COUCHDB_SERVER)
    db = server[db]

    params['include_docs'] = params.get('include_docs', True)

    counter = None
    while counter is None or counter > page:
        counter = 0
        params['limit'] = page + 1
        for row in db.view(view, **params):
            counter += 1
            if counter > page:
                params['startkey'] = row['key']
                params['startkey_docid'] = row['id']
            else:
                doc = row.pop('doc')
                yield row, doc


def listmpprofiles(args):
    params = dict(
        startkey=['MPProfile', u'\ufff0'],
        endkey=['MPProfile'],
        descending=True
    )
    for row, doc in _list_nodes('sboard/by_type', **params):
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
        for row, doc in _list_nodes('sboard/by_type', **params):
            print(u'[ %s ]: %s' % (doc['_id'], doc.get('title')))


def listbytype(args):
    types = args.types.split(',')
    counter = 0
    for type in types:
        params = dict(
            startkey=[type, u'\ufff0'],
            endkey=[type],
            descending=True
        )
        for row, doc in _list_nodes('sboard/by_type', **params):
            counter += 1
            if counter > args.limit:
                return
            else:
                print(u'[ %s ]: %s' % (
                    doc['_id'],
                    doc.get('title'),
                ))


def deletempgroups(args):
    server = Server(settings.COUCHDB_SERVER)
    db = server['nodes']

    print('Deleting groups and memberships.')
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
        for row, doc in _list_nodes('sboard/by_type', **params):
            group_id = doc['_id']
            print('DEL: [ %s ]: %s' % (group_id, doc.get('title')))
            db.delete_doc(doc)

            query = _list_nodes('profiles/group_members', startkey=[group_id], endkey=[group_id, u'\ufff0'])
            for row, doc in query:
                _ = next(query)
                if not doc:
                    continue
                print('DEL membership: [ %s ]: %s' % (doc['_id'], doc.get('profile')))
                db.delete_doc(doc)

    db = server['mps']
    print('Cleaning mps database.')
    for row, doc in _list_nodes('_all_docs', db='mps'):
        print('CLEAN: [ %s ]: %s %s' % (doc['_id'], doc.get('first_name'),
                                        doc.get('last_name')))
        for group in range(len(doc.get('groups', []))):
            if 'group_node_id' in doc['groups'][group]:
                doc['groups'][group]['group_node_id'] = None
            if 'membership_node_id' in doc['groups'][group]:
                doc['groups'][group]['membership_node_id'] = None
        db.save_doc(doc)

def listfractions(args):
    from manoseimas.mps.abbr import get_fraction_abbr

    fractions_abbr = {
        u'Frakcija "Viena Lietuva"':                                 u'VLF',
        u'"Ąžuolo" frakcija':                                        u'ĄF',
        u'Tautos prisikėlimo partijos frakcija':                     u'TPPF',
        u'Jungtinė (Liberalų ir centro sąjungos ir Tautos prisikėlimo partijos) frakcija': u'JF',
        u'Darbo partijos  frakcija':                                 u'DPF',
        u'Frakcija "Tvarka ir teisingumas"':                         u'TTF',
        u'Krikščionių partijos frakcija':                            u'KPF',
        u'Liberalų  sąjūdžio frakcija':                              u'LSF',
        u'Liberalų ir centro sąjungos frakcija':                     u'LCSF',
        u'Lietuvos socialdemokratų partijos frakcija':               u'LSDPF',
        u'Mišri Seimo narių grupė':                                  u'MG',
        u'Tėvynės sąjungos-Lietuvos krikščionių demokratų frakcija': u'TSLKDF',
    }

    type = 'Fraction'
    params = dict(
        startkey=[type, u'\ufff0'],
        endkey=[type],
        descending=True
    )
    for row, doc in _list_nodes('sboard/by_type', **params):
        title = doc.get('title')
        abbr = get_fraction_abbr(title)
        real_abbr = fractions_abbr.get(title)
        error = abbr != real_abbr
        if not args.errors or (args.errors and error):
            print(u'[ %s ]: %-8s %s' % (
                doc['_id'],
                abbr,
                title,
            ))
        if error:
            print(u'  ERROR: real abbr: %s' % real_abbr)


def syncpositions(args):
    import sboard.factory
    from manoseimas.compat.models import update_parliament_positions
    sboard.factory.autodiscover()

    update_parliament_positions()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # replicate
    p = subparsers.add_parser('replicate')
    p.add_argument('--source', default=None)
    p.add_argument('--target', default=None)
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

    # listbytype
    p = subparsers.add_parser('listbytype')
    p.add_argument('types')
    p.add_argument('--limit', type=int, default=10)
    p.set_defaults(func=listbytype)

    # listfractions
    p = subparsers.add_parser('listfractions')
    p.add_argument('--errors', action="store_true", default=False)
    p.set_defaults(func=listfractions)

    # syncpositions
    p = subparsers.add_parser('syncpositions')
    p.add_argument('solution')
    p.set_defaults(func=syncpositions)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
