# coding: utf-8
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

import itertools
from decimal import Decimal as dc

from zope.interface import implements

from sboard.factory import provideNode
from sboard.models import Node
from sboard.models import NodeProperty
from sboard.models import couch

from couchdbkit.ext.django import schema

from .interfaces import IIssue
from .interfaces import ISolution
from .interfaces import ISolutionIssue
from .interfaces import ICounterArgument


SHORT_ARGUMENT_COUNT = 3


class Solution(Node):
    implements(ISolution)

    def arguments(self):
        solves = query_solution_solves(self._id)
        raises = query_solution_raises(self._id)
        return itertools.izip_longest(solves, raises)

    def short_arguments(self):
        return list(self.arguments())[:SHORT_ARGUMENT_COUNT]

    def more_arguments(self):
        return len(list(self.arguments())) > SHORT_ARGUMENT_COUNT

provideNode(Solution, "solution")


class Issue(Node):
    implements(IIssue)

provideNode(Issue, "issue")


class SolutionIssue(Node):
    implements(ISolutionIssue)

    solution = NodeProperty()
    issue = NodeProperty()

    solves = schema.BooleanProperty()

    def counter_arguments(self):
        return list(couch.view('solutions/counter_arguments', key=self._id).iterator())

provideNode(SolutionIssue, "solution-issue")


class CounterArgument(Node):
    implements(ICounterArgument)

provideNode(CounterArgument, "counter-argument")


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


def query_solution_votings(solution_id):
    for node in couch.view('solutions/votings', key=solution_id):
        node.weight = node.solutions[solution_id]   # how the voting influences solution
        node.weight_plus_if_needed = "+" if node.weight > 0 else ""

        # was voting "accepted" - ar istatymas buvo priimtas?
        # TODO: https://bitbucket.org/manoseimas/manoseimas/issue/88/i-lrs-svetain-s-nusiurbti-info-ar

        # calculate general parliament position as one number

        node.avg_parl_position_normalized = sum([
            node.vote_aye * node.get_vote_value('aye'),
            node.vote_no * node.get_vote_value('no'),
            node.vote_abstain * node.get_vote_value('abstain'),
            node.did_not_vote() * node.get_vote_value('no-vote'),
        ]) / dc(node.registered_for_voting) / dc(2)  # normalize (divide by max amplitude -- 2)
        node.weighted_avg_parl_position = node.weight * node.avg_parl_position_normalized
        yield node
