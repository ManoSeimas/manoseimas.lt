# coding: utf-8

from __future__ import unicode_literals

from django.test import TestCase

from manoseimas.mps_v2 import helpers
from manoseimas.mps_v2.models import ParliamentMember
from manoseimas.compatibility_test.factories import TopicFactory, compatibility_test_factory


class TestHelpers(TestCase):
    maxDiff = None

    def test_get_profile_positions(self):
        topic = TopicFactory(name='Aukštojo mokslo reforma')
        compatibility_test_factory(topic, [('1', 'LSDPF', 'Petras', 'Gražulis', [1, 2])])

        # Test profile position conversion
        mp = ParliamentMember.objects.get(first_name='Petras')
        positions = helpers.get_profile_positions(mp.positions)
        self.assertEqual(positions, {
            'for': [
                {
                    'node_ref': topic.pk,
                    'permalink': '#',
                    'formatted': 'Palaiko 75%',
                    'title': 'Aukštojo mokslo reforma',
                    'position': 1.5,
                    'klass': 'strong-support',
                }
            ],
            'against': [],
            'neutral': [],
        })

        # Test old profile position format
        positions = helpers.get_profile_positions({'for': [], 'against': [], 'neutral': []})
        self.assertEqual(positions, {'for': [], 'against': [], 'neutral': []})
