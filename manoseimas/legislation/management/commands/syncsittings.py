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

import datetime
import os 
from subprocess import call

from django.conf import settings
from django.core.management.base import BaseCommand

from couchdbkit import schema
from couchdbkit.exceptions import NoResultFound
from couchdbkit.exceptions import ResourceNotFound

from manoseimas.scrapy.db import get_db
from manoseimas.votings.models import Voting, Source

from sboard.models import couch
from sboard.models import get_new_id


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


class RawVoting(schema.Document):
    datetime = DateTimeProperty()
    total_votes = schema.IntegerProperty()
    vote_abstain = schema.IntegerProperty()
    vote_aye = schema.IntegerProperty()
    vote_no = schema.IntegerProperty()
    source = schema.SchemaProperty(Source())


class SyncException(Exception):
    pass


class SyncProcessor(object):
    def __init__(self):
        self._profile_ids = {}
        self._fraction_ids = {}

    def get_voting_by_source_id(self, source_id):
        try:
            return couch.view('votings/by_source_id', key=source_id).first()
        except ResourceNotFound:
            return None

    def get_legal_act_by_number(self, number):
        try:
            return couch.view('legislation/by_number', key=number).first()
        except ResourceNotFound:
            return None

    def get_question(self, doc):
        question = get_db('question').get(doc.question)
        return question

    def get_or_create_voting(self, doc):
        voting = self.get_voting_by_source_id(doc.source.id)
        if voting is None:
            voting = Voting()
            voting._id = get_new_id()
        return voting

    def get_source(self, doc):
        voting_source_url = doc.source['url'] or ''
        if voting_source_url and not voting_source_url.startswith('http'):
            voting_source_url = ('http://www3.lrs.lt/pls/inter/' +
                                 voting_source_url)

        return {
            'voting': {
                'id': doc.source.id,
                'url': voting_source_url,
            },
        }

    def get_legal_acts(self, numbers):
        legal_acts = set()
        parent_legal_acts = set()
        for number in numbers:
            legal_act = self.get_legal_act_by_number(number)
            if legal_act is not None:
                legal_acts.add(legal_act._id)
                parent_legal_acts.update(legal_act.parents)
        return list(legal_acts), list(parent_legal_acts)

    def get_profile_id(self, source_id):
        if source_id not in self._profile_ids:
            profile = couch.view('mps/by_source_id', key=source_id).first()
            if profile:
                key = profile._id
            else:
                key = None
            self._profile_ids[source_id] = key
        return self._profile_ids[source_id]

    def get_fraction_id(self, fraction_abbreviation):
        abbr_map = {
            'TSF': 'TSLKDF',
        }
        fraction_abbreviation = abbr_map.get(fraction_abbreviation,
                                             fraction_abbreviation)
        if fraction_abbreviation not in self._fraction_ids:
            view = couch.view('mps/fraction_by_abbr',
                              key=fraction_abbreviation)
            try:
                fraction = view.one(except_all=True)
            except NoResultFound:
                return None
            if fraction.mergedto:
                fraction_id = fraction.mergedto.ref.key
            else:
                fraction_id = fraction.key
            self._fraction_ids[fraction_abbreviation] = fraction_id
        return self._fraction_ids[fraction_abbreviation]

    def sync_votes(self, votes):
        ret = {
            'aye': [],
            'abstain': [],
            'no': [],
        }
        for vote in votes:
            if vote['vote'] == 'no-vote':
                continue
            profile_id = self.get_profile_id(vote['person'].rstrip('p'))
            fraction_id = self.get_fraction_id(vote['fraction'])
            ret[vote['vote']].append([profile_id, fraction_id])
        return ret

    def save_node(self, node):
        node.save()

    def process(self, doc, update_mode=False):
        node = self.get_voting_by_source_id(doc.source.id)

        if node is None:
            node = Voting()
            node._id = get_new_id()
        elif not update_mode:
            # If the voting already exists, it means we've reached
            # the end of our new nodes. We only proceed if we're in
            # update mode.
            return False

        node.created = doc.datetime

        # TODO: Replace this with title calculation based on legal acts.
        if 'formulation' in doc:
            node.title = doc.formulation
        elif 'formulation_a' in doc:
            node.title = doc.formulation_a

        # Number of people, that has voting right
        node.has_voting_right = len(doc.votes)

        # Number of people, that registered for this voting session.
        if 'registration' in doc:
            node.registered_for_voting = int(doc.registration['joined'])

        # Total votes received.
        node.total_votes = doc.total_votes

        # Voting type (regular, urgent, ...)
        if 'type' in doc:
            node.voting_type = doc.type

        # Voting results.
        node.vote_abstain = doc.vote_abstain
        node.vote_aye = doc.vote_aye
        node.vote_no = doc.vote_no

        # List of votes by person and fraction.
        if 'votes' in doc:
            node.votes = self.sync_votes(doc.votes)

        # Involved legal acts.
        (node.legal_acts,
         node.parent_legal_acts) = self.get_legal_acts(doc.documents)

        # HM 2013-08-20: This is temporary, until we actually implement legal acts
        question = self.get_question(doc)
        node.documents = list(question['documents'])

        # Source information
        node.source = self.get_source(doc)

        self.save_node(node)

        return True

    def sync(self, view, update_mode):
        for doc in view:
            if not self.process(doc, update_mode):
                return False

        return True


class Command(BaseCommand):
    help = "Synchronize raw legal acts data with django-sboard nodes."

    def add_arguments(self, parser):
        parser.add_argument('--update',
                            action='store_true',
                            default=False,
                            help='Resync all sittings')
        parser.add_argument('--scrape',
                            action='store_true',
                            default=False,
                            help='Scrape sittings from lrs.lt')

    def handle(self, *args, **options):
        update_mode = options['update']

        if options['scrape']:
            scrapy_path = os.path.abspath(os.path.join(settings.BUILDOUT_DIR, 'bin', 'scrapy'))
            scrapy_cmd = [scrapy_path, "crawl", "sittings"]
            if update_mode:
                print "Update mode enabled. Re-scraping all sittings..."
                scrapy_cmd += ["-a", "resume=no"]
            else:
                print 'Scraping incremental sittings from lrs.lt...'

            call(scrapy_cmd)

        if update_mode:
            print "Update mode enabled. Re-syncing all sittings..."


        RawVoting.set_db(get_db('voting'))
        processor = SyncProcessor()
        has_docs = True
        last = None
        limit = 100
        params = dict(
            include_docs=True,
            limit=limit,
            classes=dict(voting=RawVoting),
        )
        while has_docs:
            view = RawVoting.view('scrapy/sequential_votings_with_documents', **params)
            rows = list(view)

            if len(rows) == limit:
                last = rows.pop()
            else:
                has_docs = False

            if not processor.sync(rows, update_mode):
                break

            if last is not None:
                params['startkey'] = last.source.id

