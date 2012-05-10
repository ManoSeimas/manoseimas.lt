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

from django.core.management.base import BaseCommand

from sboard.models import couch
from sboard.models import get_new_id
from sboard.profiles.models import MembershipNode
from sboard.utils import slugify


from manoseimas.mps.models import Commission
from manoseimas.mps.models import Committee
from manoseimas.mps.models import Fraction
from manoseimas.mps.models import MPProfile
from manoseimas.mps.models import Parliament
from manoseimas.mps.models import ParliamentaryGroup
from manoseimas.mps.models import Party
from manoseimas.scrapy.pipelines import get_db
from manoseimas.utils import todate


class SyncException(Exception):
    pass


class SyncProcessor(object):
    def __init__(self, db, verbosity=1):
        self.db = db
        self.verbosity = verbosity

    def get_node(self, node_id, node_class):
        if node_id:
            return couch.get(node_id)
        else:
            node = node_class()
            node._id = get_new_id()
            return node

    def process_groups(self, groups, profile):
        group_type_map = {
            "fraction": Fraction,
            "committee": Committee,
            "commission": Commission,
            "parliament": Parliament,
            "party": Party,
            "group": ParliamentaryGroup,
        }

        for doc in groups:
            group_node_id = doc.get('group_node_id')
            membership_node_id = doc.get('membership_node_id')

            group_type = group_type_map[doc['type']]

            if group_type is Fraction:
                importance = 10
            else:
                importance = 5

            group = self.get_node(group_node_id, group_type)
            group.slug = slugify(doc['name'])
            # TODO: extract keywords from title
            #group.keywords = ?
            group.importance = importance
            group.title = doc['name']
            group.save()

            membership = self.get_node(membership_node_id, MembershipNode)
            membership.profile = profile._id
            membership.group = group._id
            if 'membership' in doc:
                membership.term_from = todate(doc['membership'][0])
                membership.term_to = todate(doc['membership'][1])
            if 'position' in doc:
                membership.position = doc['position']
            membership.save()

            doc['group_node_id'] = group._id
            doc['membership_node_id'] = membership._id


    def process(self, doc):
        if 'doc_type' not in doc or doc['doc_type'] != 'person':
            return

        node = self.get_node(doc.get('node_id'), MPProfile)
        node.slug = slugify('%s %s' % (doc['first_name'], doc['last_name']))

        if self.verbosity >= 1:
            print 'Node %s (%s) ...' % (node._id, node.slug),

        node.keywords = node.slug.split('-')
        node.importance = 10
        node.title = u'%s %s' % (doc['first_name'], doc['last_name'])
        node.first_name = doc['first_name']
        node.last_name = doc['last_name']
        node.dob = doc.get('dob')
        node.home_page = doc.get('home_page')
        node.parliament = doc['parliament']
        node.source = doc['source']

        node.save()

        self.process_groups(doc['groups'], node)

        doc['node_id'] = node._id
        self.db.save_doc(doc)

        if self.verbosity >= 1:
            print('OK')


    def sync(self, view='_all_docs'):
        has_docs = True
        last = None
        limit = 100
        params = {'include_docs': True, 'limit': limit}
        while has_docs:
            rows = self.db.view(view, **params)
            rows = list(rows)
            if len(rows) == limit:
                last = rows.pop()
            else:
                has_docs = False

            for doc in rows:
                self.process(doc['doc'])

            if last is not None:
                params['startkey'] = last['id']


class Command(BaseCommand):
    help = "Synchronize raw legal acts data with django-sboard nodes."

    def handle(self, *args, **options):
        db = get_db('person')
        processor = SyncProcessor(db)
        processor.sync()
