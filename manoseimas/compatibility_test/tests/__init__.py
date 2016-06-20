import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from manoseimas.models import ManoSeimasUser
from manoseimas.compatibility_test.models import UserResult


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
