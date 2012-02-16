# coding: utf-8

import uuid
import datetime

from django.core.management.base import BaseCommand

from couchdbkit import schema
from couchdbkit.exceptions import ResourceNotFound
from couchdbkit.ext.django.loading import get_db

from manoseimas.votings.models import Voting, Source

from sboard.models import couch


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
    def get_id(self):
        return str(uuid.uuid4())

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

    def get_question(self):
        pass

    def get_or_create_voting(self, doc):
        voting = self.get_voting_by_source_id(doc.source.id)
        if voting is None:
            voting = Voting()
            voting._id = self.get_id()
        return voting

    def get_source(self, doc):
        voting_source_url = doc.source['url']
        if not voting_source_url.startswith('http'):
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

    def process(self, doc):
        node = self.get_or_create_voting(doc)
        node.created = doc.datetime

        if 'formulation' in doc:
            node.title = doc.formulation

        # Number of people, that has voting right
        node.has_voting_right = len(doc.votes)

        # Number of people, that registered for this voting session.
        if 'registration' in doc:
            node.registered_for_voting = int(doc.registration['joined'])

        # Total votes received.
        node.total_votes = doc.total_votes

        # Voting type (regular, urgent, ...)
        node.voting_type = doc.type

        # Voting results.
        node.vote_abstain = doc.vote_abstain
        node.vote_aye = doc.vote_aye
        node.vote_no = doc.vote_no

        # List of votes by person and fraction.
        if 'votes' in doc:
            node.votes = list(doc.votes)

        # Involved legal acts.
        (node.legal_acts,
         node.parent_legal_acts) = self.get_legal_acts(doc.documents)

        # Source information
        node.source = self.get_source(doc)

        node.save()

        print('Node: %s' % node._id)

    def sync(self, view):
        for doc in view:
            self.process(doc)


class Command(BaseCommand):
    help = "Synchronize raw legal acts data with django-sboard nodes."

    def handle(self, *args, **options):
        RawVoting.set_db(get_db('sittings'))
        processor = SyncProcessor()
        has_docs = True
        params = {'include_docs': True, 'limit': 10}
        while has_docs:
            view = RawVoting.view('scrapy/votes_with_documents', **params)
            rows = list(view)
            if len(rows) > 0:
                last = rows.pop()
                processor.sync(rows)
                params['startkey'] = last._id
            else:
                has_docs = False
