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

from zope.component import adapts
from zope.component import provideAdapter

from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from sboard.factory import getNodeFactory
from sboard.nodes import CreateView
from sboard.nodes import DetailsView
from sboard.nodes import ListView
from sboard.nodes import UpdateView
from sboard.utils import slugify

from .forms import AssignIssueForm
from .forms import AssignVotingForm
from .forms import SolutionForm
from .forms import SolutionIssueForm
from .interfaces import IIssue
from .interfaces import ISolution
from .interfaces import ISolutionIssue
from .models import Issue
from .models import query_issue_raises
from .models import query_issue_solves
from .models import query_solution_raises
from .models import query_solution_solves


def solution_nav(node, nav, active):
    active = active or ('index',)

    nav.append({
        'key': 'node-title',
        'title': _('Sprendimas'),
        'header': True,
    })

    key = 'index'
    nav.append({
        'key': key,
        'url': node.permalink(),
        'title': _('Sprendimas'),
        'children': [],
        'active': key in active,
    })

    key = 'votings'
    nav.append({
        'key': key,
        'url': node.permalink(key),
        'title': _('Balsavimai'),
        'children': [],
        'active': key in active,
    })

    return nav


class SolutionDetailsView(DetailsView):
    adapts(ISolution)

    template = 'solutions/node_details.html'

    def nav(self, active=tuple()):
        nav = super(SolutionDetailsView, self).nav(active)
        return solution_nav(self.node, nav, active)

    def render(self, **overrides):
        solves = query_solution_solves(self.node._id)
        raises = query_solution_raises(self.node._id)
        context = {
            'issues': itertools.izip_longest(solves, raises),
        }
        context.update(overrides)
        return super(SolutionDetailsView, self).render(**context)

provideAdapter(SolutionDetailsView)


class SolutionVotingsView(ListView):
    adapts(ISolution)
    template = 'solutions/votings_list.html'

    def nav(self, active=tuple()):
        if not active:
            active = ('votings',)
        nav = super(SolutionVotingsView, self).nav(active)
        return solution_nav(self.node, nav, active)

    def get_node_list(self):
        return self.node.get_votings()

    def render(self, **overrides):
        if self.request.method == 'POST':
            form = AssignVotingForm(self.request.POST)
            if form.is_valid():
                voting = form.cleaned_data.get('voting')
                solution = self.node
                position = form.cleaned_data.get('position')
                solutions = voting.solutions or {}
                solutions[solution._id] = position

                voting.solutions = solutions
                voting.save()

                return redirect(self.node.permalink('votings'))
        else:
            form = AssignVotingForm()

        context = {
            'form': form,
        }
        context.update(overrides)
        return super(SolutionVotingsView, self).render(**context)

provideAdapter(SolutionVotingsView, name="votings")


class CreateSolutionView(CreateView):
    adapts(object, ISolution)

    form = SolutionForm

provideAdapter(CreateSolutionView, name="create")


class AssignSolutionIssue(CreateView):
    form = AssignIssueForm

    def __init__(self, node):
        self.node = node  # solution
        self.factory = getNodeFactory('solution-issue')

    def before_save(self, form, node, create):
        if not node.issue:
            issue = Issue()
            issue.set_new_id()
            issue.slug = slugify(node.title)
            issue.title = node.title
            issue.save()
            node.issue = issue

        # Title is never saved for SolutionIssue, it is taken from Issue.
        node.title = None
        solves = 'sprendimas' if self.solves else 'priezastis'
        node.slug = '%s-%s-%s' % (node.issue.ref.get_slug(), solves,
                                  self.node.get_slug())
        node.solves = self.solves
        node.solution = self.node


class AssignSolvingIssue(AssignSolutionIssue):
    adapts(ISolution)

    solves = True

provideAdapter(AssignSolvingIssue, name="sprendzia")


class AssignRaisingIssue(AssignSolutionIssue):
    adapts(ISolution)

    solves = False

provideAdapter(AssignRaisingIssue, name="sukelia")


class SolutionIssueListView(DetailsView):
    adapts(ISolution)

    def nav(self, active=tuple()):
        if not active:
            active = ('issues',)
        nav = super(SolutionIssueListView, self).nav(active)
        return solution_nav(self.node, nav, active)

provideAdapter(SolutionIssueListView, name="issues")


class SolutionIssueDetailsView(DetailsView):
    adapts(ISolutionIssue)

    template = 'solutions/solution_issue_details.html'

    def render(self, **overrides):
        solves = query_issue_solves(self.node.issue._id)
        raises = query_issue_raises(self.node.issue._id)
        context = {
            'title': self.node.issue.ref.title,
            'solutions': itertools.izip_longest(solves, raises),
        }
        context.update(overrides)
        return super(SolutionIssueDetailsView, self).render(**context)

provideAdapter(SolutionIssueDetailsView)


class SolutionIssueUpdateView(UpdateView):
    adapts(ISolutionIssue)
    form = SolutionIssueForm

provideAdapter(SolutionIssueUpdateView, name='update')


class IssueDetailsView(DetailsView):
    adapts(IIssue)

    template = 'solutions/issue_details.html'

    def render(self, **overrides):
        solves = query_issue_solves(self.node._id)
        raises = query_issue_raises(self.node._id)
        context = {
            'solutions': itertools.izip_longest(solves, raises),
        }
        context.update(overrides)
        return super(IssueDetailsView, self).render(**context)

provideAdapter(IssueDetailsView)
