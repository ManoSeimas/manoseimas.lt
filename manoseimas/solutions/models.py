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

from zope.interface import implements

from sboard.factory import provideNode
from sboard.models import Node
from sboard.models import NodeProperty
from sboard.models import couch

from couchdbkit.ext.django import schema

from .interfaces import IIssue
from .interfaces import ISolution
from .interfaces import ISolutionIssue


class Solution(Node):
    implements(ISolution)

    def get_votings(self):
        return couch.view('solutions/votings', key=self._id)

    def mps_positions(self):
        """Returns dict with position of each MP for this solution.

        Positions are calculated from assigned votings for this solutions.

        """
        mps = {}
        view = couch.view('solutions/votings', key=self._id)
        # Loop for all votings
        for voting in view:
            position = voting.solutions[self._id]
            # Loop for all vote values (aye, abstain, no)
            for vote_value, votes in voting.votes.items():
                vote_value = voting.get_vote_value(vote_value)
                # Loop for each MP vote
                for mp_id, fraction_id in votes:
                    if mp_id not in mps:
                        mps[mp_id] = {'times': 0, 'sum': 0}

                    mps[mp_id]['times'] += abs(position)
                    mps[mp_id]['sum'] += vote_value * position

        return dict([(mp_id, 1.0 * mp['sum'] / mp['times'])
                     for mp_id, mp in mps.items()])

provideNode(Solution, "solution")


class Issue(Node):
    implements(IIssue)

provideNode(Issue, "issue")


class SolutionIssue(Node):
    implements(ISolutionIssue)

    solution = NodeProperty()
    issue = NodeProperty()

    solves = schema.BooleanProperty()

provideNode(SolutionIssue, "solution-issue")


def query_solution_issues(solution_id, solves):
    """Returns iterator over SolutionIssue nodes prepopulated with issue nodes
    for issue attribute of SolutionIssue node.

    Nodes are sorted by likes and SolutionIssue id in descending order.
    """
    kwargs = dict(
        startkey=[solution_id, solves, {}],
        endkey=[solution_id, solves],
        descending=True
    )
    query = couch.view('solutions/issues', **kwargs).iterator()
    for node in query:
        issue = next(query)
        node.issue = issue
        yield node


def query_solution_solves(solution_id):
    return query_solution_issues(solution_id, solves=True)


def query_solution_raises(solution_id):
    return query_solution_issues(solution_id, solves=False)


def query_issue_solutions(issue_id, solves):
    """Returns iterator over SolutionIssue nodes prepopulated with solution
    nodes for solution attribute of SolutionIssue node.

    Nodes are sorted by likes and SolutionIssue id in descending order.
    """
    kwargs = dict(
        startkey=[issue_id, solves, {}],
        endkey=[issue_id, solves],
        descending=True
    )
    query = couch.view('solutions/by_issue', **kwargs).iterator()
    for node in query:
        solution = next(query)
        node.solution = solution
        yield node


def query_issue_solves(issue_id):
    return query_issue_solutions(issue_id, solves=True)


def query_issue_raises(issue_id):
    return query_issue_solutions(issue_id, solves=False)