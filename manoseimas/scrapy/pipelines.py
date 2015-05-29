import datetime

from manoseimas.scrapy.db import get_db, get_doc, store_doc
from manoseimas.scrapy.items import Person

from manoseimas.mps_v2.models import ParliamentMember, PoliticalParty
from manoseimas.mps_v2.models import Group, GroupMembership


def is_latest_version(item, doc):
    item_version = item.get('source', {}).get('version')
    doc_version = doc.get('source', {}).get('version')
    if not item_version or not doc_version:
        return True

    return item_version >= doc_version


class ManoseimasPipeline(object):

    def process_item(self, item, spider):
        if '_id' not in item or not item['_id']:
            raise Exception('Missing doc _id. Doc: %s' % item)

        item_name = item.__class__.__name__.lower()
        db = get_db(item_name)

        doc = get_doc(db, item['_id'])
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
        store_doc(db, doc)

        return item


class ManoSeimasModelPersistPipeline(object):

    def process_mp(self, item, spider):
        source_url = item['source']['url']

        mp = ParliamentMember(
            source_id=item['_id'],
            first_name=item['first_name'],
            last_name=item['last_name'],
            date_of_birth=item.get('dob'),
            email=item.get('email', [None])[0],
            phone=item.get('phone', [None])[0],
            candidate_page=item.get('home_page'),
            term_of_office=item.get('parliament', [None])[0],
            office_address=item['office_address'],
            constituency=item['constituency'],
            party_candidate=item.get('party_candidate', True),
            biography=item.get('biography'),
            source=source_url
        )
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

    def process_item(self, item, spider):
        if isinstance(item, Person):
            return self.process_mp(item, spider)
        else:
            return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass
