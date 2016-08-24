# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import itertools

from django_webtest import WebTest
import factory

from django.core.urlresolvers import reverse
from django.test import TestCase

from manoseimas.scrapy.models import PersonVote

from manoseimas.factories import AdminUserFactory
from manoseimas.models import ManoSeimasUser
from manoseimas.mps_v2.models import Group, ParliamentMember
from manoseimas.mps_v2.factories import GroupFactory, ParliamentMemberFactory, GroupMembershipFactory
from manoseimas.compatibility_test.models import UserResult
from manoseimas.compatibility_test.views import topics_all
from manoseimas.compatibility_test import factories


class TestAnswersJson(WebTest):
    csrf_checks = False

    def test_answers_json_get(self):
        self.assertEqual(ManoSeimasUser.objects.count(), 0)
        test = factories.CompatTestFactory()
        resp = self.app.get(reverse('answers_json', kwargs={'test_id': test.id}))
        self.assertEqual(resp.json, {'answers': {}, 'test_id': test.id})
        # lazy user is created
        self.assertEqual(ManoSeimasUser.objects.count(), 1)
        self.assertEqual(UserResult.objects.count(), 0)

    def test_answers_json_post(self):
        answers = {
            '1': 'yes',
            '2': 'no',
        }
        test = factories.CompatTestFactory()
        resp = self.app.post_json(
            reverse('answers_json', kwargs={'test_id': test.id}),
            answers
        )
        user = ManoSeimasUser.objects.first()
        self.assertEqual(resp.json, {'answers': answers, 'test_id': test.id})
        # lazy user is created
        self.assertEqual(ManoSeimasUser.objects.count(), 1)
        # answers are saved
        self.assertEqual(UserResult.objects.count(), 1)
        ur = UserResult.objects.first()
        self.assertEqual(ur.user, user)
        self.assertEqual(ur.result, answers)


class TestCompatibilityTest(TestCase):
    def test_topics_all(self):
        test = factories.CompatTestFactory()
        topic = factories.TopicFactory()
        factories.TestGroupFactory(test=test, topics=[topic])
        factories.TopicFactory(name='Darbo kodeksas')

        self.assertEqual(topics_all(test.id), [
            {
                'id': topic.pk,
                'group': 'Socialiniai reikalai',
                'name': 'Aukštojo mokslo reforma',
                'slug': 'aukstojo-mokslo-reforma',
                'description': 'Aukštojo mokslo reforma',
                'arguments': [],
                'votings': [],
                'image': None,
            },
        ])


class TestViews(WebTest):
    maxDiff = None
    csrf_checks = False

    def test_index_view(self):
        topic = factories.TopicFactory()
        factories.TopicVotingFactory.create_batch(3, topic=topic)
        group = factories.TestGroupFactory(topics=[topic])
        resp = self.app.get('/testas/')
        self.assertRedirects(resp, '/testas/%d/' % group.test.id)
        resp = resp.follow()
        self.assertEqual(resp.html.title.string, 'Politinių pažiūrų testas - manoSeimas.lt')

    def test_results_view(self):
        tp1, tp2 = topics = [
            factories.TopicFactory(name='Socialinis modelis'),
            factories.TopicFactory(name='Kariuomenė'),
        ]

        data = [
            ('1', 'DP', 'Jonas', 'Jonaitis', [1, -0.3]),
            ('2', 'DP', 'Petras', 'Petraitis', [1, 0.5]),
            ('3', 'LLS', 'Jonas', 'Petraitis', [-0.8, 1]),
        ]

        genpos = lambda positions: {topic.pk: position for topic, position in zip(topics, positions)}

        GroupFactory(abbr='DP', name='Darbo partijos frakcija', positions=genpos([1, 0.3]))
        GroupFactory(abbr='LLS', name='Liberalų sąjūdžio frakcija', positions=genpos([0.5, -0.3]))

        mps = []
        for p_asm_id, fraction, first_name, last_name, positions in data:
            group = Group.objects.get(abbr=fraction)
            mp = ParliamentMemberFactory(
                source_id=p_asm_id,
                first_name=first_name,
                last_name=last_name,
                term_of_office='2012-2016',
                positions=genpos(positions),
            )
            GroupMembershipFactory(member=mp, group=group)
            mps.append(mp)

        mp1, mp2, mp3 = mps
        gr1, gr2 = Group.objects.filter(abbr__in=['DP', 'LLS']).order_by('pk')

        test = factories.CompatTestFactory()
        factories.TestGroupFactory(topics=topics, test=test)

        resp = self.app.post(reverse('test_results', kwargs={'test_id': test.id}))

        fractions = [{
            'title': x['title'],
            'short_title': x['short_title'],
            'answers': {int(k): v for k, v in x['answers'].items()},
            'members_amount': x['members_amount'],
        } for x in resp.json['fractions']]
        self.assertEqual(fractions, [
            {
                'title': 'Darbo partijos frakcija',
                'short_title': 'DP',
                'answers': {int(tp1.pk): 1, int(tp2.pk): 0.3},
                'members_amount': 2,
            },
            {
                'title': 'Liberalų sąjūdžio frakcija',
                'short_title': 'LLS',
                'answers': {int(tp1.pk): 0.5, int(tp2.pk): -0.3},
                'members_amount': 1,
            },
        ])

        mps = [{
            'name': x['name'],
            'fraction': x['fraction'],
            'answers': {int(k): v for k, v in x['answers'].items()},
        } for x in resp.json['mps']]
        self.assertEqual(mps, [
            {
                'name': 'Jonas Jonaitis',
                'fraction': 'DP',
                'answers': {int(tp1.pk): 1, int(tp2.pk): -0.3}
            },
            {
                'name': 'Petras Petraitis',
                'fraction': 'DP',
                'answers': {int(tp1.pk): 1, int(tp2.pk): 0.5}
            },
            {
                'name': 'Jonas Petraitis',
                'fraction': 'LLS',
                'answers': {int(tp1.pk): -0.8, int(tp2.pk): 1}
            },
        ])

    def test_results_view_answers(self):
        answers = {
            '1': 'yes',
            '2': 'no',
        }
        topics = factories.TopicFactory.create_batch(
            2,
            name=factory.Iterator(['Socialinis modelis', 'Kariuomenė']),
        )
        test = factories.CompatTestFactory()
        factories.TestGroupFactory(topics=topics, test=test)
        resp = self.app.post(reverse('test_results', kwargs={'test_id': test.id}))
        self.assertEqual(resp.json['user_answers'], None)

        ur = factories.UserResultFactory(result=answers)
        self.app.set_user(ur.user)
        resp = self.app.post(reverse('test_results', kwargs={'test_id': test.id}))
        self.assertEqual(resp.json['user_answers'], answers)


class TestPositions(WebTest):
    maxDiff = None

    def test_position(self):
        AdminUserFactory()

        votings = []
        seq = itertools.count(1)
        topic = factories.TopicFactory()
        factories.TestGroupFactory(topics=[topic])
        mps = [
            ('1', 'LSDPF', 'Petras', 'Gražulis', [1, 2]),
            ('2', 'LSDPF', 'Mantas', 'Adomėnas', [-2, 2]),
            ('3', 'TS-LKDF', 'Remigijus', 'Ačas', [-2, 0, -1]),
        ]

        GroupFactory(abbr='LSDPF', name='Lietuvos socialdemokratų partijos frakcija')
        GroupFactory(abbr='TS-LKDF', name='Tėvynės sąjungos-Lietuvos krikščionių demokratų frakcija')

        # Create some votings and assigne them to the topic
        for i in range(3):
            voting = factories.VotingFactory()
            factories.TopicVotingFactory(topic=topic, voting=voting)
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
                    timestamp=datetime.datetime(2012, 11, 16),
                )

        # Save topic from Django admin
        url = reverse('admin:compatibility_test_topic_change', args=[topic.pk])
        resp = self.app.get(url, user='admin')
        resp.forms['topic_form'].submit('_save')

        # Check if ParliamentMember positions where updated.
        gr = lambda x: {int(k): float(v) for k, v in Group.objects.get(abbr=x).positions.items()}
        mp = lambda x: {int(k): float(v) for k, v in ParliamentMember.objects.get(first_name=x).positions.items()}
        self.assertEqual(gr('LSDPF'), {topic.pk: 0.75})
        self.assertEqual(gr('TS-LKDF'), {topic.pk: -1.0})
        self.assertEqual(mp('Petras'), {topic.pk: 1.5})
        self.assertEqual(mp('Mantas'), {topic.pk: 0.0})
        self.assertEqual(mp('Remigijus'), {topic.pk: -1.0})
