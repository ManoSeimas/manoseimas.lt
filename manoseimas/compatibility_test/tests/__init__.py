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
from manoseimas.compatibility_test.models import Topic
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
                'description': 'Aukštojo mokslo reforma',
                'arguments': [],
                'votings': [],
            },
        ])


class TestViews(WebTest):
    csrf_checks = False

    def test_index_view(self):
        topic = factories.TopicFactory()
        factories.TopicVotingFactory.create_batch(3, topic=topic)
        group = factories.TestGroupFactory(topics=[topic])
        resp = self.app.get('/test/')
        self.assertRedirects(resp, '/test/%d/' % group.test.id)
        resp = resp.follow()
        self.assertEqual(resp.html.title.string, 'Politinio suderinamumo testas - manoSeimas.lt')

    def test_results_view(self):
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
        mps = [
            ('1', 'FOO', 'First Last', [1, 2]),
            ('2', 'FOO', 'Second Last', [-2, 2]),
            ('3', 'BAR', 'Third Last', [-2, 0, -1]),
        ]

        # Create some votings and assigne them to the topic
        for i in range(3):
            voting = factories.VotingFactory()
            factories.TopicVotingFactory(topic=topic, voting=voting)
            votings.append(voting)

        # Create person votes for topic and votings
        for p_asm_id, fraction, name, votes in mps:
            for i, vote in enumerate(votes):
                PersonVote.objects.create(
                    key=str(next(seq)),
                    voting_id=votings[i].key,
                    p_asm_id=p_asm_id,
                    fraction=fraction,
                    name=name,
                    vote=vote,
                    timestamp=datetime.datetime(2012, 11, 16),
                )

        # Save topic from Django admin
        url = reverse('admin:compatibility_test_topic_change', args=[topic.pk])
        resp = self.app.get(url, user='admin')
        resp.forms['topic_form'].submit('_save')

        # Check if topic position was updated.
        topic = Topic.objects.get(pk=topic.pk)
        self.assertEqual(topic.positions, {
            '1': {
                'fraction': 'FOO',
                'name': 'First Last',
                'vote': 1.5,
            },
            '2': {
                'fraction': 'FOO',
                'name': 'Second Last',
                'vote': 0,
            },
            '3': {
                'fraction': 'BAR',
                'name': 'Third Last',
                'vote': -1,
            },
        })
