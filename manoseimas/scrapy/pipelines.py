# -*- coding: utf-8 -*-
import datetime
import functools
import os

from django.db import transaction
from django.core.files.base import ContentFile
from django.conf import settings

from scrapy.item import Item

import manoseimas.common.utils.words as words_utils

from manoseimas.scrapy.items import (
    Person, StenogramTopic, ProposedLawProjectProposer,
    Lobbyist, LobbyistDeclaration, Suggestion)
from manoseimas.scrapy.helpers.stenograms import get_voting_for_stenogram
from manoseimas.scrapy.helpers.stenograms import get_votings_by_date
from manoseimas.scrapy import models

from manoseimas.mps_v2.abbr import get_fraction_abbr
from manoseimas.mps_v2.models import ParliamentMember, PoliticalParty
from manoseimas.mps_v2.models import Group, GroupMembership
from manoseimas.mps_v2.models import Stenogram, StenogramStatement
from manoseimas.mps_v2.models import StenogramTopic as StenogramTopicModel
from manoseimas.mps_v2.models import Voting, LawProject
from manoseimas.mps_v2.models import Suggestion as SuggestionModel
from manoseimas.mps_v2.models import Suggester as SuggesterModel
from manoseimas.mps_v2.models import CommitteeResolution

import manoseimas.lobbyists.models as lobbyists_models


def is_latest_version(item, doc):
    item_version = item.get('source', {}).get('version')
    doc_version = doc.get('source', {}).get('version')
    if not item_version or not doc_version:
        return True

    return item_version >= doc_version


def check_spider_pipeline(process_item_method):

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        # if class is in the spider's pipeline, then use the
        # process_item method normally.
        if self.__class__ in getattr(spider, 'pipelines', []) or spider is None:
            return process_item_method(self, item, spider)
        else:
            return item

    return wrapper


def save_item(item):
    pipeline = ManoseimasPipeline()
    if isinstance(item, Item):
        pipeline.process_item(item, None)
        item_name = pipeline.get_item_name()
        Model = pipeline.models[item_name]
        return Model.objects.get(key=item['_id'])
    else:
        item_name = item['doc_type'].lower()
        Model = pipeline.models[item_name]
        instance = Model()
        instance.update_from_item(item)
        instance.save()
        return instance


class ManoseimasPipeline(object):
    models = {
        'person': models.Person,
        'voting': models.Voting,
        'question': models.Question,
        'personvote': models.PersonVote,
    }

    def open_spider(self, spider):
        pass

    def get_item_name(self, item):
        return item.__class__.__name__.lower()

    @check_spider_pipeline
    def process_item(self, item, spider):
        if '_id' not in item or not item['_id']:
            raise Exception('Missing doc _id. Doc: %s' % item)

        item_name = self.get_item_name(item)
        Model = self.models[item_name]

        _item = dict(item)
        attachments = _item.pop('_attachments', None) or []

        try:
            obj = Model.objects.get(key=_item['_id'])
        except Model.DoesNotExist:
            obj = Model()

        # Some documents contain source versioning. In those cases,
        # we must ensure we're not clobbering a newer sourced
        # document with an older version.
        if not is_latest_version(_item, obj.value):
            return

        obj.update_from_item(_item)
        obj.save()

        for name, stream, mime in attachments:
            path = os.path.join(settings.MEDIA_ROOT, 'attachments', item_name, str(obj.pk))
            if not os.path.exists(path):
                os.makedirs(path)
            stream.seek(0)
            with open(os.path.join(path, name), 'wb') as f:
                f.write(stream.read())

        return item


class MPNameMatcher(object):

    def __init__(self):
        all_mps = ParliamentMember.objects.all()
        self.mp_names = {u'{}. {}'.format(mp.first_name[:1].upper(),
                                          mp.last_name.upper()): mp
                         for mp in all_mps}
        full_names = {mp.full_name.upper(): mp
                      for mp in all_mps}
        self.mp_names.update(full_names)
        reversed_names = {' '.join([mp.last_name, mp.first_name]).upper(): mp
                          for mp in all_mps}
        self.mp_names.update(reversed_names)

    def get_mp_by_name(self, mp_name, fraction=None):
        mp_name = mp_name.upper()
        mp = self.mp_names.get(mp_name)
        if not mp:
            parts = mp_name.split(' ')
            if len(parts) > 2:
                new_mp_name = ' '.join((parts[0], parts[-1]))
                mp = self.mp_names.get(new_mp_name.upper())
            elif len(parts) == 2:
                # Handle double last names with a dash instead of a space
                last_name = parts[-1]
                adjusted_last_name = ' '.join(last_name.split('-'))
                new_mp_name = ' '.join([parts[0], adjusted_last_name])
                mp = self.mp_names.get(new_mp_name.upper())
        return mp


class LobbyistNameMatcher(object):

    def __init__(self):
        all_lobbyists = lobbyists_models.Lobbyist.objects.all()
        self.by_name = {self.canonical_name(l.name): l
                        for l in all_lobbyists}

    def get_lobbyist_by_name(self, name):
        return self.by_name.get(self.canonical_name(name))

    @staticmethod
    def canonical_name(name):
        return name.upper().translate({
            ord(u'"'): None,
            ord(u'„'): None,
            ord(u'“'): None,
            ord(u'”'): None,
        })


class ManoSeimasModelPersistPipeline(object):

    @transaction.atomic
    def process_mp(self, item, spider):
        source_url = item['source']['url']

        mp, created = ParliamentMember.objects.get_or_create(
            source_id=item['_id'],
            defaults={
                'first_name': item['first_name'],
                'last_name': item['last_name'],
            }
        )

        mp.first_name = item['first_name']
        mp.last_name = item['last_name']
        mp.date_of_birth = item.get('dob')
        mp.email = item.get('email', [None])[0]
        phone = item.get('phone', [None])[0]
        if phone:
            mp.phone = phone[:32]
        mp.candidate_page = item.get('home_page')
        mp.term_of_office = item.get('parliament', [None])[0]
        mp.office_address = item['office_address']
        mp.constituency = item['constituency']
        mp.party_candidate = item.get('party_candidate', True)
        mp.biography = item.get('biography')
        mp.source = source_url

        image = (item.get('images') or [None])[0]

        if image:
            image_base = spider.settings['IMAGES_STORE']
            photo_path = os.path.join(image_base, image['path'])
            data = ContentFile(open(photo_path, 'rb').read())
            mp.photo.save(os.path.basename(image['path']), data)

        if item['raised_by']:
            party, __ = PoliticalParty.objects.get_or_create(
                name=item['raised_by'],
                defaults={'source': source_url}
            )
            mp.raised_by = party
        mp.save()

        for item_group in item['groups']:
            group, created = Group.objects.get_or_create(
                name=item_group['name'],
                type=item_group['type'],
                defaults={'source': source_url}
            )
            if group.type == Group.TYPE_FRACTION:
                group.abbr = get_fraction_abbr(group.name)
            group.save()
            item_membership = item_group.get('membership')
            membership, __ = GroupMembership.objects.get_or_create(
                member=mp,
                group=group,
                position=item_group['position'],
                since=item_membership[0] if item_membership else None,
            )
            if item_membership:
                membership.until = item_membership[1]
            membership.source = source_url
            membership.save()
        return item

    @transaction.atomic
    def process_stenogram_topic(self, item, spider):
        source_url = item['source']['url']

        stenogram, created = Stenogram.objects.get_or_create(
            source_id=item['_id'],
            defaults={
                'date': item['date'],
                'sitting_no': item['sitting_no'],
                'sitting_name': item.get('sitting_name'),
                'session': item.get('session'),
                'source': source_url,
            }
        )
        if not created and not stenogram.session and item.get('session'):
            stenogram.session = item['session']
            stenogram.save()

        # TODO: need a robust mechanism to uniquely identify topics
        # inside a stenogam. Or maybe just drop it entirely
        topic, created = StenogramTopicModel.objects.get_or_create(
            stenogram=stenogram,
            title=item['title'],
            defaults={
                'source': source_url,
                'timestamp': item['date'],
            }
        )

        if not created:
            topic.votings.all().delete()

        # Find voting for this stenogram topic
        votings = get_votings_by_date(item['date'].date())
        docs = get_voting_for_stenogram(votings, item['title'], item['date'])

        presenter_names = set()
        for doc in docs:
            for document in doc.value.get('documents', []):
                for speaker in document.get('speakers', []):
                    presenter_names.add(speaker['name'])
            Voting.objects.create(stenogram_topic=topic, voting=doc, timestamp=doc.timestamp)
        presenters = filter(bool,
                            map(self.mp_matcher.get_mp_by_name,
                                list(presenter_names)))
        topic.presenters = presenters
        topic.save()

        # Recreate all the statements since we can't reliably
        # identify statements in the database now
        topic.statements.all().delete()
        for statement in item['statements']:
            speaker = self.mp_matcher.get_mp_by_name(statement['speaker'])
            text = u' '.join(statement['statement'])
            statement = StenogramStatement(
                topic=topic,
                speaker=speaker,
                speaker_name=statement['speaker'],
                text=text,
                source=source_url,
                as_chairperson=statement['as_chair'],
                word_count=words_utils.get_word_count(text)
            )
            statement.save()

        return item

    @transaction.atomic
    def process_proposed_law_project(self, item, spider):
        source_url = item['source']['url']
        mp = self.mp_matcher.get_mp_by_name(item['proposer_name'])
        if not mp:
            # If we dont know this MP there is nothing we can do.
            # We will receive this project with another MP
            print(u'Bailing because no mp: {}'.format(item['proposer_name']))
            return item
        proposal, created = LawProject.objects.get_or_create(
            source_id=item['id'],
            defaults={'date': item['date'],
                      'project_name': item['project_name'],
                      'project_number': item['project_number'],
                      'project_url': item['project_url'],
                      'source': source_url}
        )
        proposal.proposers.add(mp)
        passing = item.get('passed')
        if passing:
            proposal.date_passed = passing['passing_date']
            proposal.passing_source_id = passing['id']
            proposal.passing_number = passing.get('passing_number')
            proposal.passing_url = passing['source']['url']

        proposal.save()

        return item

    @transaction.atomic
    def process_lobbyist(self, item, spider):
        lobbyist, created = lobbyists_models.Lobbyist.objects.get_or_create(
            name=item['name'],
            # some fields cannot be null
            defaults=dict(
                date_of_inclusion=item['date_of_inclusion'],
            )
        )
        lobbyist.representatives = item.get('representatives') or ''
        lobbyist.url = item.get('url') or ''
        lobbyist.company_code = item.get('company_code') or ''
        lobbyist.date_of_inclusion = item['date_of_inclusion']
        lobbyist.decision = item['decision']
        lobbyist.status = item.get('status') or ''
        lobbyist.source = item['source_url']
        lobbyist.raw_data = item['raw_data']
        lobbyist.save()
        return item

    @transaction.atomic
    def process_lobbyist_declaration(self, item, spider):
        declaration, created = lobbyists_models.LobbyistDeclaration.objects.get_or_create(
            lobbyist_name=item['name'],
            year=item['year'],
        )
        lobbyist = self.lobbyist_matcher.get_lobbyist_by_name(item['name'])
        if lobbyist is not None:
            declaration.lobbyist = lobbyist
        declaration.comments = item.get('comments') or ''
        declaration.source = item['source_url']
        declaration.raw_data = item['raw_data']
        declaration.save()
        if not created:
            # re-create the clients and topics on every scrape
            declaration.clients.all().delete()
        for client_item in item.get('clients', []):
            client = declaration.clients.create(name=client_item['client'])
            for project in client_item['law_projects']:
                client.law_projects.create(title=project)
        if item.get('law_projects'):
            client = declaration.clients.create(name='-')
            for project in item['law_projects']:
                client.law_projects.create(title=project)
        return item

    @transaction.atomic
    def process_suggestion(self, item, spider):
        suggester, created = SuggesterModel.objects.get_or_create(
            title=item['submitter'],
            defaults={'source': item['source_url']},
        )
        if not suggester.source:
            suggester.source = item['source_url']
            suggester.save()
        resolution, created = CommitteeResolution.objects.get_or_create(
            source_id=item['source_id'],
            defaults={'source': item['source_url']},
        )
        if not resolution.source:
            resolution.source = item['source_url']
        resolution.title = item['source_title']
        resolution.save()
        suggestion, created = SuggestionModel.objects.get_or_create(
            source_resolution=resolution,
            source_index=item['source_index'],
        )
        suggestion.submitter.add(suggester)
        suggestion.date = item['date'] or None
        suggestion.document = item['document']
        suggestion.opinion = item['opinion']
        suggestion.source = item['source_url']
        suggestion.save()
        return item

    @check_spider_pipeline
    def process_item(self, item, spider):
        if isinstance(item, Person):
            return self.process_mp(item, spider)
        elif isinstance(item, StenogramTopic):
            return self.process_stenogram_topic(item, spider)
        elif isinstance(item, ProposedLawProjectProposer):
            return self.process_proposed_law_project(item, spider)
        elif isinstance(item, Lobbyist):
            return self.process_lobbyist(item, spider)
        elif isinstance(item, LobbyistDeclaration):
            return self.process_lobbyist_declaration(item, spider)
        elif isinstance(item, Suggestion):
            return self.process_suggestion(item, spider)
        else:
            return item

    def open_spider(self, spider):
        self.mp_matcher = MPNameMatcher()
        self.lobbyist_matcher = LobbyistNameMatcher()
