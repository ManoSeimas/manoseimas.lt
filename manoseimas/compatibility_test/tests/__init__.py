# coding: utf-8

from __future__ import absolute_import
from __future__ import unicode_literals

from django_webtest import WebTest

from django.core.urlresolvers import reverse
from django.test import TestCase

from manoseimas.models import ManoSeimasUser
from manoseimas.compatibility_test.models import UserResult
from manoseimas.compatibility_test.views import topics_all
from manoseimas.compatibility_test import factories


class TestAnswersJson(WebTest):
    csrf_checks = False

    def test_answers_json_get(self):
        self.assertEqual(ManoSeimasUser.objects.count(), 0)
        resp = self.app.get(reverse('answers_json'))
        user = ManoSeimasUser.objects.first()
        self.assertEqual(resp.json, {'answers': {}, 'user': user.pk})
        # lazy user is created
        self.assertEqual(ManoSeimasUser.objects.count(), 1)
        self.assertEqual(UserResult.objects.count(), 0)

    def test_answers_json_post(self):
        answers = {'answers': [
            ['1', 'yes'],
            ['2', 'no'],
        ]}
        resp = self.app.post_json(reverse('answers_json'), answers)
        user = ManoSeimasUser.objects.first()
        self.assertEqual(resp.json, {'answers': answers, 'user': user.pk})
        # lazy user is created
        self.assertEqual(ManoSeimasUser.objects.count(), 1)
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
