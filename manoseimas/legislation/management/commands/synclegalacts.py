# coding: utf-8

import datetime

from django.core.management.base import BaseCommand

from couchdbkit.exceptions import ResourceNotFound, ResourceConflict

from manoseimas.legal_acts.models import LegalAct
from manoseimas.legislation.models import Law, LawChange, LawProject
from manoseimas.legislation.utils import normalize, split_law_name

from sboard.models import couch
from sboard.utils import get_node_id


class SyncException(Exception):
    pass


class SyncProcessor(object):
    def __init__(self):
        self.relations = {}

    def get_by_number(self, number):
        try:
            return couch.view('legislation/by_number', key=number).first()
        except ResourceNotFound:
            return None

    def get_by_cleaned_name(self, cleaned_name):
        try:
            return couch.view('legislation/by_cleaned_name',
                              key=cleaned_name).first()
        except ResourceNotFound:
            return None

    def get_parents(self, split=None):
        parents = []
        split = split or []
        for cleaned_name in split:
            node = self.get_by_cleaned_name(cleaned_name)
            if node is not None:
                parents.append(node._id)
        return parents

    def date_to_datetime(self, date):
        return datetime.datetime.combine(date, datetime.time())

    def update_node(self, cls, legal_act, node_id, split=None):
        node = self.get_by_number(legal_act.number)
        if node is None:
            node = cls()
            node._id = node_id

        node.number = legal_act.number
        node.title = legal_act.name
        node.cleaned_name = normalize(legal_act.name)
        node.body = legal_act.current_version()
        node.created = self.date_to_datetime(legal_act.date)
        node.parents = self.get_parents(split)


        try:
            node.save()
        except ResourceConflict:
            pass
            # TODO: Some leagal acts can have same name, but different numbers.
            # This must be some how handlerd.
            #
            # Possible solution - sync all legal acts starting from oldest, if
            # a legal act with same name exists, then track it as history node
            # with an update that comes with newer legal act with same name.


        print('Node: %s' % node._id)

    def process_law(self, legal_act):
        node_id = get_node_id(legal_act.name)
        self.update_node(Law, legal_act, node_id)

    def process_law_change(self, legal_act, split):
        node_id = get_node_id()
        self.update_node(LawChange, legal_act, node_id, split)

    def process_law_project(self, legal_act, split):
        node_id = get_node_id()
        self.update_node(LawProject, legal_act, node_id, split)

    def process(self, legal_act):
        if 'kind' not in legal_act:
            continue
            # TODO: examine documents, that does not have 'kind' attribute
            #raise SyncException("Document does not have 'kind' attribute.")

        if 'name' not in legal_act:
            continue
            # TODO: examine documents, that does not have 'name' attribute
            #raise SyncException("Document does not have 'name' attribute.")

        split = split_law_name(legal_act.name)

        law_kinds = (u'įstatymas', u'konstitucija', u'statutas', u'kodeksas')

        if legal_act.kind == u'įstatymo projektas':
            self.process_law_project(legal_act, split)

        elif legal_act.kind in law_kinds:
            if split:
                self.process_law_change(legal_act, split)
            else:
                self.process_law(legal_act)

        else:
            raise SyncException("Unknown 'kind' attribute: %s" % legal_act.kind)

    def sync(self, view):
        for legal_act in view:
            self.process(legal_act)


class Command(BaseCommand):
    help = "Synchronize raw legal acts data with django-sboard nodes."

    def handle(self, *args, **options):
        view = LegalAct.view('_all_docs', include_docs=True)
        processor = SyncProcessor()
        processor.sync(view)
