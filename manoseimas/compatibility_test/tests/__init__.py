# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

import json

from django_webtest import WebTest

from django.core.urlresolvers import reverse
from django.test import TestCase

from manoseimas.models import ManoSeimasUser
from manoseimas.compatibility_test.models import UserResult
from manoseimas.compatibility_test.views import topics_all
from manoseimas.compatibility_test import factories


class TestAnswersJson(TestCase):
    def test_answers_json_get(self):
        self.assertEqual(ManoSeimasUser.objects.count(), 0)
        response = self.client.get(reverse('answers_json'))
        self.assertEqual(response.content, "{}")
        # lazy user is created
        self.assertEqual(ManoSeimasUser.objects.count(), 1)
        self.assertEqual(UserResult.objects.count(), 0)

    def test_answers_json_post(self):
        answers = {'answers': [
            ['1', 'yes'],
            ['2', 'no'],
        ]}
        answers_json = json.dumps(answers)
        response = self.client.post(
            reverse('answers_json'),
            data=answers_json,
            content_type='application/json'
        )
        self.assertEqual(response.content, answers_json)
        # lazy user is created
        self.assertEqual(ManoSeimasUser.objects.count(), 1)
        user = ManoSeimasUser.objects.first()
        # results are saved
        self.assertEqual(UserResult.objects.count(), 1)
        ur = UserResult.objects.first()
        self.assertEqual(ur.user, user)
        self.assertEqual(ur.result, answers)


class TestCompatibilityTest(TestCase):
    def test_topics_all(self):
        topic = factories.TopicFactory()
        factories.TestGroupFactory(topics=[topic])

        self.assertEqual(topics_all(), [
            {
                'id': topic.pk,
                'group': 'Socialiniai reikalai',
                'name': 'Aukštojo mokslo reforma',
                'description': '',
                'arguments': [],
                'votings': [],
            },
        ])


class TestViews(WebTest):
    def test_index_view(self):
        topic = factories.TopicFactory()
        factories.TopicVotingFactory.create_batch(3, topic=topic)
        factories.TestGroupFactory(topics=[topic])
        resp = self.app.get('/test/')
        self.assertEqual(resp.html.title.string, 'Politinio suderinamumo testas - manoSeimas.lt')
