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

from django.utils.translation import ugettext_lazy as _

from sboard.factory import getNodeFactory
from sboard.nodes import CreateView
from sboard.nodes import DetailsView
from sboard.nodes import UpdateView
from sboard.utils import slugify

from .forms import AssignIssueForm
from .forms import SolutionForm
from .forms import SolutionIssueForm
from .forms import CounterArgumentForm
from .interfaces import IIssue
from .interfaces import ISolution
from .interfaces import ISolutionIssue
from .interfaces import ICounterArgument
from .models import Issue
from .models import query_issue_raises
from .models import query_issue_solves


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

    key = 'seimo-pozicija'
    nav.append({
        'key': key,
        'url': node.permalink(key),
        'title': _('Seimo pozicija'),
        'children': [],
        'active': key in active,
    })

    key = 'balsavimai'
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
        context = {
            'issues': self.node.issues(),
        }
        context.update(overrides)
        return super(SolutionDetailsView, self).render(**context)

provideAdapter(SolutionDetailsView)


class SolutionCreateView(CreateView):
    adapts(object, ISolution)

    form = SolutionForm

provideAdapter(SolutionCreateView, name="create")


class SolutionUpdateView(UpdateView):
    adapts(ISolution)

    form = SolutionForm

provideAdapter(SolutionUpdateView, name="update")


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


class CounterArgumentCreateView(CreateView):
    adapts(ISolutionIssue, ICounterArgument)

    form = CounterArgumentForm

    def get_form(self, *args, **kwargs):
        kwargs['initial'] = {
            'parent': self.node.urlslug(),
        }
        return self.form(None, *args, **kwargs)

    def before_save(self, form, node, create):
        # Counterarguments lack titles, so create slug using summary.
        node.slug = slugify(node.summary)

provideAdapter(CounterArgumentCreateView, name="create")


class CounterArgumentUpdateView(UpdateView):
    adapts(ICounterArgument)

    form = CounterArgumentForm

provideAdapter(CounterArgumentUpdateView, name="update")
