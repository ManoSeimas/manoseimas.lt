import datetime

from django.db import transaction

from manoseimas.scrapy.db import get_db, get_doc, store_doc
from manoseimas.scrapy.items import Person, StenogramTopic

from manoseimas.mps_v2.models import ParliamentMember, PoliticalParty
from manoseimas.mps_v2.models import Group, GroupMembership
from manoseimas.mps_v2.models import Stenogram, StenogramStatement
from manoseimas.mps_v2.models import StenogramTopic as StenogramTopicModel


def is_latest_version(item, doc):
    item_version = item.get('source', {}).get('version')
    doc_version = doc.get('source', {}).get('version')
    if not item_version or not doc_version:
        return True

    return item_version >= doc_version


class ManoseimasPipeline(object):

    def store_item(self, db, doc, item):
        store_doc(db, doc)

    def get_doc(self, db, item):
        return get_doc(db, item['_id'])

    def process_item(self, item, spider):
        if '_id' not in item or not item['_id']:
            raise Exception('Missing doc _id. Doc: %s' % item)

        item_name = item.__class__.__name__.lower()
        db = get_db(item_name)

        doc = self.get_doc(db, item)
        if doc is None:
            doc = dict(item)
            doc['doc_type'] = item_name
        else:
            # Some documents contain source versioning. In those cases,
            # we must ensure we're not clobbering a newer sourced
            # document with an older version.
            if not is_latest_version(item, doc):
                return

            doc.update(item)

        doc['updated'] = datetime.datetime.now().isoformat()
        self.store_item(db, doc, item)

        return item


class MPNameMatcher(object):

    def __init__(self):
        self.mp_names = {u'{}. {}'.format(mp.first_name[:1].upper(),
                                          mp.last_name.upper()): mp
                         for mp in ParliamentMember.objects.all()}

    def get_mp_by_name(self, mp_name, fraction=None):
        mp = self.mp_names.get(mp_name)
        return mp


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
        mp.phone = item.get('phone', [None])[0]
        mp.candidate_page = item.get('home_page')
        mp.term_of_office = item.get('parliament', [None])[0]
        mp.office_address = item['office_address']
        mp.constituency = item['constituency']
        mp.party_candidate = item.get('party_candidate', True)
        mp.biography = item.get('biography')
        mp.source = source_url

        if item['raised_by']:
            party, __ = PoliticalParty.objects.get_or_create(
                name=item['raised_by'],
                defaults={'source': source_url}
            )
            mp.raised_by = party
        mp.save()

        for item_group in item['groups']:
            group, __ = Group.objects.get_or_create(
                name=item_group['name'],
                type=item_group['type'],
                defaults={'source': source_url}
            )
            membership, __ = GroupMembership.objects.get_or_create(
                member=mp,
                group=group,
                position=item_group['position']
            )
            item_membership = item_group.get('membership')
            if item_membership:
                membership.since = item_membership[0]
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
                'source': source_url,
            }
        )

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

        # Recreate all the statements since we can't reliably
        # identify statements in the database now
        topic.statements.all().delete()
        for statement in item['statements']:
            speaker = self.mp_matcher.get_mp_by_name(statement['speaker'])
            statement = StenogramStatement(
                topic=topic,
                speaker=speaker,
                speaker_name=statement['speaker'],
                text=u' '.join(statement['statement']),
                source=source_url,
            )
            statement.save()

        return item

    def process_item(self, item, spider):
        if isinstance(item, Person):
            return self.process_mp(item, spider)
        elif isinstance(item, StenogramTopic):
            return self.process_stenogram_topic(item, spider)
        else:
            return item

    def open_spider(self, spider):
        self.mp_matcher = MPNameMatcher()

    def close_spider(self, spider):
        pass
