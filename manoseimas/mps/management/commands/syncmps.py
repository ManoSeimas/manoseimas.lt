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

import os.path
import urllib
import glob
import os 
from subprocess import call

from django.core.management.base import BaseCommand
from django.conf import settings

from sboard.models import ImageNode
from sboard.models import couch
from sboard.models import get_new_id
from sboard.models import get_node_by_slug
from sboard.profiles.models import MembershipNode
from sboard.profiles.models import query_group_membership
from sboard.utils import slugify


from manoseimas.mps.abbr import get_fraction_abbr
from manoseimas.mps.models import Commission
from manoseimas.mps.models import Committee
from manoseimas.mps.models import Fraction
from manoseimas.mps.models import MPProfile
from manoseimas.mps.models import Parliament
from manoseimas.mps.models import ParliamentaryGroup
from manoseimas.mps.models import Party
from manoseimas.scrapy.db import get_db
from manoseimas.utils import todate


class SyncException(Exception):
    pass


class SyncProcessor(object):
    def __init__(self, db, verbosity=1):
        self.db = db
        self.verbosity = verbosity
        self._nodes = {}
        self._profiles = {}

    def _get_node(self, node_id, node_class):
        if node_id:
            return couch.get(node_id)
        else:
            node = node_class()
            node._id = get_new_id()
            return node

    def _cache_node(self, node, key):
        key = (node.doc_type, key)
        self._nodes[key] = node

    def make_node(self, node_class):
        return self._get_node(None, node_class)

    def get_node(self, node_id, node_class, key=None):
        if key is None:
            return self._get_node(node_id, node_class)

        if isinstance(key, tuple):
            key = (node_class.__name__,) + key
        else:
            key = (node_class.__name__, key)

        if key not in self._nodes:
            self._nodes[key] = self._get_node(node_id, node_class)

        return self._nodes[key]

    def get_image_node(self, profile):
        if profile.image:
            node = profile.image.ref
        else:
            node = self.get_node(None, ImageNode)
        node.title = profile.title
        node.set_parent(profile)
        node.importance = 0
        return node

    def set_image_from_file(self, profile, filename):
        image = open(filename, 'rb')
        node = self.get_image_node(profile)
        node.ext = os.path.splitext(filename)[1][1:]
        node.save()
        node.put_attachment(image, 'file.%s' % node.ext)
        image.close()
        profile.image = node

    def set_image_from_url(self, profile, url):
        node = self.get_image_node(profile)
        node.ext = os.path.splitext(url)[1][1:]
        path = node.path(fetch=False)

        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            os.makedirs(parent)

        urllib.urlretrieve(url, path)
        self.set_image_from_file(profile, path)
    
    def get_profile_node(self, source_id):
        if source_id not in self._profiles:
            profile = couch.view('mps/by_source_id', key=source_id).first()
            self._profiles[source_id] = profile
        return self._profiles[source_id]

    def get_group_by_slug(self, slug):
        node = get_node_by_slug(slug)
        if node:
            self._cache_node(node, slug)

        return node

    def get_membership_node(self, group, profile):
        # FIXME: This is a massive bottleneck for syncmps.
        # It is necessary because we lack an adequate
        # index in the couch. We need to add a view to accomodate
        # this basic query.
        for node in query_group_membership(group._id):
            if node.profile == profile:
                return node

    def process_groups(self, groups, profile, update_mode=False):
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

            slug = slugify(doc['name'])

            first_time = (group_type.__name__, slug) not in self._nodes

            if not update_mode and group_node_id:
                group = self.get_node(group_node_id, group_type, slug)
                if group.slug != slug:
                    group.slug = slug
            else:
                group = self.get_group_by_slug(slug)
                
            if not group:
                group = self.make_node(group_type)
                group.slug = slug


            # TODO: extract keywords from title
            #group.keywords = ?
            group.title = doc['name']

            if first_time:
                image_filenames = glob.glob(settings.PROJECT_DIR + u'/images/fractions/' + slug + u'.*')
                if image_filenames:
                    self.set_image_from_file(group, image_filenames[0])

            if group_type == Fraction and not group.abbreviation:
                group.abbreviation = get_fraction_abbr(group.title)

            group.save()

            if not update_mode and membership_node_id:
                membership = self.get_node(membership_node_id, MembershipNode)
            else:
                membership = self.get_membership_node(group, profile)

            if not membership:
                membership = self.make_node(MembershipNode)

            membership.profile = profile
            membership.group = group
            if 'membership' in doc:
                membership.term_from = todate(doc['membership'][0])
                membership.term_to = todate(doc['membership'][1])
            if 'position' in doc:
                membership.position = doc['position']
            membership.save()

            if group_type == Fraction and membership.is_current():
                profile.fraction = group

            doc['group_node_id'] = group._id
            doc['membership_node_id'] = membership._id

    def process(self, doc, update_mode=False):
        if 'doc_type' not in doc or doc['doc_type'] != 'person':
            return

        if doc.get('node_id') and not update_mode:
            node = self.get_node(doc.get('node_id'), MPProfile)
        else:
            node = self.get_profile_node( doc['source']['id'] )
        
        if not node:
            node = self.make_node(MPProfile)


        node.slug = slugify('%s %s' % (doc['first_name'], doc['last_name']))

        if self.verbosity >= 1:
            print 'Node %s (%s) ...' % (node._id, node.slug)

        node.keywords = node.slug.split('-')
        node.title = u'%s %s' % (doc['first_name'], doc['last_name'])
        node.first_name = doc['first_name']
        node.last_name = doc['last_name']
        node.dob = doc.get('dob')
        node.home_page = doc.get('home_page')
        node.parliament = doc['parliament']
        node.source = doc['source']
        self.set_image_from_url(node, doc['photo'])

        self.process_groups(doc['groups'], node, update_mode)

        node.save()

        doc['node_id'] = node._id
        self.db.save_doc(doc)

        if self.verbosity >= 1:
            print('OK')


    def sync(self, view='_all_docs', update_mode=False):
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
                self.process(doc['doc'], update_mode)

            if last is not None:
                params['startkey'] = last['id']


class Command(BaseCommand):
    help = "Synchronize raw legal acts data with django-sboard nodes."

    def handle(self, *args, **options):
        update_mode = "update" in args

        if "scrape" in args:
            print "Scraping all MPs from lrs.lt..."
            scrapy_path = os.path.abspath(os.path.join(settings.BUILDOUT_DIR, 'bin', 'scrapy'))
            call([scrapy_path, "crawl", "mps"])

        if update_mode:
            print "Update mode enabled. Re-syncing all MPs..."

        db = get_db('person')
        processor = SyncProcessor(db)
        processor.sync('_all_docs', update_mode)

