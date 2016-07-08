# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import collections

from django.conf import settings

from manoseimas.mps_v2.models import Group, ParliamentMember
from manoseimas.scrapy.models import PersonVote


def get_topic_positions():
    # {
    #     'fractions': {Group.id: {Topic.id: position}},
    #     'mps': {ParliamentMember.id: {Topic.id: position}},
    # }
    positions = {
        'fractions': collections.defaultdict(lambda: collections.defaultdict(int)),
        'mps': collections.defaultdict(lambda: collections.defaultdict(int)),
    }

    # {Group.abbr: Group.id}
    fractions = dict(Group.objects.filter(type=Group.TYPE_FRACTION).values_list('abbr', 'id'))

    # {PersonVote.p_asm_id: ParliamentMember.id}
    term_of_office = '{0:%Y}-{1:%Y}'.format(*settings.TERM_OF_OFFICE_RANGE)
    mps = dict(ParliamentMember.objects.filter(term_of_office=term_of_office).values_list('source_id', 'id'))

    groups = [
        (fractions, 'fractions', 'fraction', 'PersonVote.fraction'),
        (mps, 'mps', 'p_asm_id', 'PersonVote.p_asm_id, PersonVote.fraction'),
    ]
    for idmapping, key, attr, groupby in groups:
        # This raw SQL query is needed, because PersonVote.voting_id -> Voting.key does not have proper foreign key.
        # If someone fixes Scrapy pipeline to use PersonVote.voting -> Voting as foreign key, this raw SQL query can be
        # rewritten to Django ORM.
        results = PersonVote.objects.raw('''
            SELECT
                NULL as id,
                {groupby},
                TopicVoting.topic_id,
                SUM(PersonVote.vote * TopicVoting.factor) / SUM(ABS(TopicVoting.factor)) AS position
            FROM scrapy_personvote AS PersonVote
            INNER JOIN scrapy_voting AS Voting ON Voting.key = PersonVote.voting_id
            INNER JOIN compatibility_test_topicvoting AS TopicVoting ON TopicVoting.voting_id = Voting.id
            WHERE PersonVote.timestamp BETWEEN %(since)s AND %(until)s
            GROUP BY {groupby}, TopicVoting.topic_id
            HAVING SUM(ABS(TopicVoting.factor)) > 0
        '''.format(groupby=groupby), {
            'since': settings.TERM_OF_OFFICE_RANGE.since.strftime('%Y-%m-%d'),
            'until': settings.TERM_OF_OFFICE_RANGE.until.strftime('%Y-%m-%d'),
        })
        for vote in results:
            try:
                positions[key][idmapping[getattr(vote, attr)]][vote.topic_id] = vote.position
            except KeyError as e:
                print((
                    'KeyError: positions[%(key)r][idmapping[%(attr)r]->%(id)s][%(topic_id)r] = %(position)r, error: %(error)s'
                ) % {
                    'id': idmapping.get(getattr(vote, attr, None)),
                    'key': key,
                    'attr': getattr(vote, attr),
                    'topic_id': vote.topic_id,
                    'position': vote.position,
                    'error': e,
                })

    return positions


def update_topic_positions(results):
    for group_id, positions in results['fractions'].items():
        group = Group.objects.get(pk=group_id)
        group.positions = positions
        group.save()

    for mp_id, positions in results['mps'].items():
        mp = ParliamentMember.objects.get(pk=mp_id)
        mp.positions = positions
        mp.save()
