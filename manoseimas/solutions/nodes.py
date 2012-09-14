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
from operator import attrgetter

from zope.component import adapts
from zope.component import provideAdapter

from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from sboard.factory import getNodeFactory
from sboard.models import get_node_by_slug
from sboard.nodes import CreateView
from sboard.nodes import DetailsView
from sboard.nodes import UpdateView
from sboard.nodes import ListView
from sboard.utils import slugify

from manoseimas.compat.models import PersonPosition
from manoseimas.compat.models import update_parliament_positions
from manoseimas.compat.models import calculate_solution_parliament_avg_position
from manoseimas.compat.models import fetch_positions
from manoseimas.compat.nodes import TEST_BUTTONS
from manoseimas.compat.nodes import adapt_position

from .forms import AssignIssueForm
from .forms import SolutionForm
from .forms import SolutionIssueForm
from .forms import CounterArgumentForm
from .forms import AssignVotingForm
from .interfaces import IIssue
from .interfaces import ISolution
from .interfaces import ISolutionIssue
from .interfaces import ICounterArgument
from .models import Issue
from .models import query_issue_raises
from .models import query_issue_solves
from .models import query_solution_raises
from .models import query_solution_solves
from .models import query_solution_votings


def solution_nav(node, nav, active):
    active = active or ('index',)

    nav.append({
        'key': 'node-title',
        'title': _('Tema'),
        'header': True,
    })

    key = 'index'
    nav.append({
        'key': key,
        'url': node.permalink(),
        'title': _(u'Aprašymas'),
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
        node, position, clipped, important = adapt_position(
                next(fetch_positions(self.request, [self.node])))
        context = {
            'arguments': self.node.arguments(),
            'buttons': TEST_BUTTONS,
            'position': position,
            'clipped': clipped,
            'important': important,
        }
        context.update(overrides)
        return super(SolutionDetailsView, self).render(**context)

provideAdapter(SolutionDetailsView)


class MPsPositionView(DetailsView):
    adapts(ISolution)
    template = 'solutions/mps_position.html'

    def nav(self, active=tuple()):
        active = active or ('seimo-pozicija')
        nav = super(MPsPositionView, self).nav(active)
        return solution_nav(self.node, nav, active)

    def render(self, **overrides):
        solution_id = self.node._id
        mps = PersonPosition.objects.mp_pairs(solution_id)
        fractions = map(list, PersonPosition.objects.fraction_pairs(solution_id))
        fraction_list = [pp.profile.ref for pp in itertools.chain(fractions[0], fractions[1])]
        fraction_list.sort(key=attrgetter('title'))
        context = {
            'groups': (
                {
                    'title': _('Frakcijos'),
                    'slug': 'frakcijos',
                    'positions': fractions,
                },
                {
                    'title': _('Seimo nariai'),
                    'slug': 'seimo-nariai',
                    'positions': mps,
                    'fraction_list': fraction_list,
                },
            ),
        }
        context.update(overrides)
        return super(MPsPositionView, self).render(**context)

provideAdapter(MPsPositionView, name='seimo-pozicija')


class SolutionVotingsView(ListView):
    adapts(ISolution)
    template = 'solutions/votings_list.html'

    def nav(self, active=tuple()):
        if not active:
            active = ('balsavimai',)
        nav = super(SolutionVotingsView, self).nav(active)
        return solution_nav(self.node, nav, active)

    def get_node_list(self):
        return list(query_solution_votings(self.node._id))

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

                PersonPosition.objects.filter(node=solution._id).delete()
                update_parliament_positions(solution._id)

                return redirect(self.node.permalink('balsavimai'))
        else:
            form = AssignVotingForm()

        parl_weighted_position, parl_normalized_position = calculate_solution_parliament_avg_position(self.node._id)
        context = {
            'form': form,
            'parl_weighted_position': parl_weighted_position,
            'parl_normalized_position': parl_normalized_position,
        }
        context.update(overrides)
        return super(SolutionVotingsView, self).render(**context)

provideAdapter(SolutionVotingsView, name="balsavimai")


class UnassignVotingView(ListView):
    adapts(ISolution, unicode)
    template = 'solutions/votings_list.html'

    def __init__(self, node, voting_id):
        self.voting_id = voting_id
        super(UnassignVotingView, self).__init__(node)

    def render(self, **overrides):
        voting = get_node_by_slug(self.voting_id)
        if voting:
            if self.node._id in voting.solutions:
                del voting.solutions[self.node._id]
                voting.save()
                PersonPosition.objects.filter(node=self.node._id).delete()
                update_parliament_positions(self.node._id)
            return redirect(self.node.permalink('balsavimai'))
        else:
            raise Http404

provideAdapter(UnassignVotingView, name="delete")


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


def solution_issue_nav(node, nav, active):
    if node.solution:
        nav.append({
            'key': 'node-title',
            'title': _('Argumentas'),
            'header': True,
        })

        for arg in query_solution_solves(node.solution._id):
            key = arg.key
            nav.append({
                'key': key,
                'class': 'positive',
                'url': arg.permalink(),
                'title': arg.issue.ref.title,
                'children': [],
                'active': key in active,
            })

        for arg in query_solution_raises(node.solution._id):
            key = arg.key
            nav.append({
                'key': key,
                'class': 'negative',
                'url': arg.permalink(),
                'title': arg.issue.ref.title,
                'children': [],
                'active': key in active,
            })

    return nav


class SolutionIssueDetailsView(DetailsView):
    adapts(ISolutionIssue)

    template = 'solutions/solution_issue_details.html'

    def nav(self, active=None):
        if not active:
            active = (self.node.key,)
        nav = super(SolutionIssueDetailsView, self).nav(active)
        return solution_issue_nav(self.node, nav, active)

    def render(self, **overrides):
        if self.node.issue:
            title = self.node.issue.ref.title
        else:
            title = self.node.title
        context = {
            'title': title,
        }
        context.update(overrides)
        return super(SolutionIssueDetailsView, self).render(**context)

provideAdapter(SolutionIssueDetailsView)


class SolutionIssueCreateView(CreateView):
    adapts(object, ISolutionIssue)
    form = SolutionIssueForm

provideAdapter(SolutionIssueCreateView, name='create')

class SolutionIssueUpdateView(UpdateView):
    adapts(ISolutionIssue)
    form = SolutionIssueForm
    template = 'solutions/solution_issue_form.html'

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


class CounterArgumentView(DetailsView):
    adapts(ICounterArgument)

    template = 'solutions/counter_argument.html'

provideAdapter(CounterArgumentView)


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
