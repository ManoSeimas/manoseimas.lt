# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.

from django.core.urlresolvers import reverse
from django.test import TestCase

from sboard.tests import NodesTestsMixin

from manoseimas.votings.models import Voting
from manoseimas.votings.tests import load_fixtures

from .models import Issue
from .models import Solution
from .models import SolutionIssue
from .models import query_issue_raises
from .models import query_issue_solves
from .models import query_solution_raises
from .models import query_solution_solves


class SolutionTests(NodesTestsMixin, TestCase):
    def testSolutions(self):
        db = Voting.get_db()
        load_fixtures(db)

        self._login_superuser()

        # Create new solution
        response = self._create('solution', title='S1', _f=('body',))
        self.assertRedirects(response, reverse('node', args=['~']))


        # Visit voting page
        v1_id = '16aa1e75-a5fb-4233-9213-4ddcc0380fe5'
        v1_url = reverse('node', args=[v1_id])
        response = self.client.get(v1_url)
        self.assertEqual(response.status_code, 200)


        # Link voting to solution
        v1_link_url = reverse('node', args=[v1_id, 'link-solution'])
        response = self.client.post(v1_link_url, {
            'solution': 's1',
            'position': '-1',
        })
        self.assertRedirects(response, v1_url)


        # Link voting to solution
        v2_id = '7b2427c4-4304-4230-a284-f63a126f8e5d'
        v2_url = reverse('node', args=[v2_id])
        v2_link_url = reverse('node', args=[v2_id, 'link-solution'])
        response = self.client.post(v2_link_url, {
            'solution': 's1',
            'position': '-3',
        })
        self.assertRedirects(response, v2_url)


        # TODO: move this part to compat app
        ## Try to get user voting match results
        #results_url = reverse('node', args=['s1', 'submit-position'])
        #response = self.client.get(results_url, {'vote': '2'})
        #self.assertEqual(response.status_code, 200)
        #data = json.loads(response.content)
        #self.assertEqual(data['mps'][0]['id'], '000078')
        #self.assertEqual(data['mps'][0]['score'], 87)


def create_solution(title):
    node = Solution()
    node.set_new_id()
    node.title = title
    node.save()
    return node


def create_issue(title):
    node = Issue()
    node.set_new_id()
    node.title = title
    node.save()
    return node


def create_solution_issue(solution, issue, summary, solves, likes=0):
    node = SolutionIssue()
    node.set_new_id()
    node.solution = solution
    node.issue = issue
    node.summary = 'Solution 1 solves Issue 1'
    node.solves = solves
    node.likes = likes
    node.save()
    return node


def solution_solves(solution, issue, summary, likes=0):
    return create_solution_issue(solution, issue, summary, solves=True,
                                 likes=likes)


def solution_raises(solution, issue, summary, likes=0):
    return create_solution_issue(solution, issue, summary, solves=False,
                                 likes=likes)


class SolutionIssuesTests(NodesTestsMixin, TestCase):

    def test_solution_issues(self):
        issue_1 = create_issue('Issue 1')
        issue_2 = create_issue('Issue 2')
        issue_3 = create_issue('Issue 3')
        issue_4 = create_issue('Issue 4')
        issue_5 = create_issue('Issue 5')

        solution_1 = create_solution('Solution 1')

        # Solution 1 solves:
        solves_1_1 = solution_solves(solution_1, issue_1,
                                     'Solution 1 solves Issue 1', likes=9)
        solves_1_2 = solution_solves(solution_1, issue_2,
                                     'Solution 1 solves Issue 2', likes=8)

        # Solution 1 raises:
        raises_1_3 = solution_raises(solution_1, issue_3,
                                     'Solution 1 raises Issue 3', likes=9)
        raises_1_4 = solution_raises(solution_1, issue_4,
                                     'Solution 1 raises Issue 4', likes=9)
        raises_1_5 = solution_raises(solution_1, issue_5,
                                     'Solution 1 raises Issue 5', likes=7)

        solves = query_solution_solves(solution_1._id)
        solves = list(solves)

        self.assertEqual(solves[0]._id, solves_1_1._id)
        self.assertEqual(solves[0].issue.ref.title, 'Issue 1')
        self.assertEqual(solves[1]._id, solves_1_2._id)
        self.assertEqual(solves[1].issue.ref.title, 'Issue 2')

        solves = query_solution_raises(solution_1._id)
        solves = list(solves)

        self.assertEqual(solves[0]._id, raises_1_4._id)
        self.assertEqual(solves[0].issue.ref.title, 'Issue 4')
        self.assertEqual(solves[1]._id, raises_1_3._id)
        self.assertEqual(solves[1].issue.ref.title, 'Issue 3')
        self.assertEqual(solves[2]._id, raises_1_5._id)
        self.assertEqual(solves[2].issue.ref.title, 'Issue 5')

    def test_issues(self):
        issue_1 = create_issue('Issue 1')

        solution_1 = create_solution('Solution 1')
        solution_2 = create_solution('Solution 2')
        solution_3 = create_solution('Solution 3')

        # Issue 1 may be raised by:
        raises_1_1 = solution_raises(solution_1, issue_1,
                                     'Solution 1 raises Issue 1', likes=9)

        # Issue 1 can be solved by:
        solves_2_1 = solution_solves(solution_2, issue_1,
                                     'Solution 2 solves Issue 1', likes=9)
        solves_3_1 = solution_solves(solution_3, issue_1,
                                     'Solution 3 solves Issue 1', likes=8)

        # Raised by
        raises = query_issue_raises(issue_1._id)
        raises = list(raises)

        self.assertEqual(len(raises), 1)
        self.assertEqual(raises[0]._id, raises_1_1._id)
        self.assertEqual(raises[0].solution.ref.title, 'Solution 1')

        # Solved by
        solves = query_issue_solves(issue_1._id)
        solves = list(solves)

        self.assertEqual(len(solves), 2)
        self.assertEqual(solves[0]._id, solves_2_1._id)
        self.assertEqual(solves[0].solution.ref.title, 'Solution 2')
        self.assertEqual(solves[1]._id, solves_3_1._id)
        self.assertEqual(solves[1].solution.ref.title, 'Solution 3')
