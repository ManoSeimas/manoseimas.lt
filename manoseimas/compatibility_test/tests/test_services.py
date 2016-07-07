# coding: utf-8

from __future__ import unicode_literals

import datetime
import itertools

from django.test import TestCase

from manoseimas.scrapy.models import PersonVote
from manoseimas.mps_v2.models import Group, ParliamentMember
from manoseimas.mps_v2.factories import GroupFactory, ParliamentMemberFactory, GroupMembershipFactory
from manoseimas.compatibility_test.factories import TopicFactory, VotingFactory, TopicVotingFactory
from manoseimas.compatibility_test import services


class TestServices(TestCase):
    maxDiff = None

    def test_position(self):
        votings = []
        seq = itertools.count(1)
        topic = TopicFactory()
        mps = [
            ('1', 'LSDPF', 'Petras', 'Gražulis', [1, 2]),
            ('2', 'LSDPF', 'Mantas', 'Adomėnas', [-2, 2]),
            ('3', 'TS-LKDF', 'Remigijus', 'Ačas', [-2, 0, -1]),
        ]

        GroupFactory(abbr='LSDPF', name='Lietuvos socialdemokratų partijos frakcija')
        GroupFactory(abbr='TS-LKDF', name='Tėvynės sąjungos-Lietuvos krikščionių demokratų frakcija')

        # Create some votings and assign them to the topic
        for i in range(3):
            voting = VotingFactory()
            TopicVotingFactory(topic=topic, voting=voting)
            votings.append(voting)

        # Create person votes for topic and votings
        for p_asm_id, fraction, first_name, last_name, votes in mps:
            group = Group.objects.get(abbr=fraction)
            mp = ParliamentMemberFactory(
                source_id=p_asm_id,
                first_name=first_name,
                last_name=last_name,
                term_of_office='2012-2016',
            )
            GroupMembershipFactory(member=mp, group=group)
            for i, vote in enumerate(votes):
                PersonVote.objects.create(
                    key=str(next(seq)),
                    voting_id=votings[i].key,
                    p_asm_id=p_asm_id,
                    fraction=fraction,
                    name='%s %s' % (first_name, last_name),
                    vote=vote,
                    timestamp=datetime.datetime(2015, 1, 1),
                )

        # Save topic from Django admin
        results = services.get_topic_positions()
        namefn = {
            'fractions': lambda x: Group.objects.get(pk=x).abbr,
            'mps': lambda x: ParliamentMember.objects.get(pk=x).first_name,
        }
        results = {
            k: {
                namefn[k](key): {
                    x: float(val) for x, val in value.items()
                } for key, value in v.items()
            } for k, v in results.items()
        }
        self.assertEqual(results, {
            'fractions': {
                'LSDPF': {topic.pk: 0.75},
                'TS-LKDF': {topic.pk: -1.0},
            },
            'mps': {
                'Petras': {topic.pk: 1.5},
                'Mantas': {topic.pk: 0.0},
                'Remigijus': {topic.pk: -1.0},
            }
        })
