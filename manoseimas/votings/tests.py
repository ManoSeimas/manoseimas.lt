import os
import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from sboard.tests import NodesTestsMixin

from .models import Voting


def load_fixtures(db):
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'fixtures', 'voting.json')) as f:
        db.save_docs(json.load(f))


class SolutionTests(NodesTestsMixin, TestCase):
    def testSolutions(self):
        db = Voting.get_db()
        load_fixtures(db)

        self._login_superuser()

        # Create new solution
        response = self._create('solution', title='S1', _f=('body',))
        self.assertRedirects(response, reverse('node_details', args=['~']))


        # Visit voting page
        v1_id = '16aa1e75-a5fb-4233-9213-4ddcc0380fe5'
        v1_url = reverse('node_details', args=[v1_id])
        response = self.client.get(v1_url)
        self.assertEqual(response.status_code, 200)


        # Link voting to solution
        v1_link_url = reverse('node_action', args=[v1_id, 'link-solution'])
        response = self.client.post(v1_link_url, {
            'solution': 's1',
            'weight': '1',
        })
        self.assertRedirects(response, v1_url)


        # Link voting to solution
        v2_id = '16aa1e75-a5fb-4233-9213-4ddcc0380fe5'
        v2_url = reverse('node_details', args=[v2_id])
        v2_link_url = reverse('node_action', args=[v2_id, 'link-solution'])
        response = self.client.post(v2_link_url, {
            'solution': 's1',
            'weight': '1',
        })
        self.assertRedirects(response, v2_url)
