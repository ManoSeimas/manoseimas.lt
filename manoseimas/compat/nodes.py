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

from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from sboard.ajax import AjaxView
from sboard.json import json_response
from sboard.models import get_node_by_slug
from sboard.models import prefetch_nodes
from sboard.nodes import DetailsView
from sboard.nodes import ListView
from sboard.nodes import NodeView
from sboard.nodes import UpdateView

from manoseimas.solutions.interfaces import ISolution
from manoseimas.solutions.nodes import solution_nav

from .forms import AssignSolutionsForm
from .forms import AssignVotingForm
from .forms import CompatNodeForm
from .interfaces import ICompat
from .models import PersonPosition
from .models import query_solution_votings
from .models import update_mps_positions


def solution_compat_nav(node, category, nav, active=tuple()):
    if not active and category:
        active = (category,)

    if category:
        nav.append({
            'key': 'node-title',
            'title': _('Testas'),
            'header': True,
        })

        key = 'assign-solutions'
        nav.append({
            'key': key,
            'url': node.permalink(category, key),
            'title': _('Priskirti sprendimus'),
            'children': [],
            'active': key in active,
        })

    if node.categories:
        nav.append({
            'key': 'sritys',
            'title': _('Sritys'),
            'header': True,
        })

        for slug, category in node.categories:
            nav.append({
                'key': slug,
                'url': node.permalink(slug),
                'title': category['title'],
                'children': [],
                'active': slug in active,
            })

    return nav


class SolutionCompatView(ListView):
    adapts(ICompat)

    template = 'votings/question_group.html'

    def __init__(self, node, category=None):
        super(SolutionCompatView, self).__init__(node)
        # Use first category if not set, by default.
        if not category and node.categories:
            category = node.categories[0][0]
        self.category = category

    def nav(self, active=tuple()):
        nav = super(SolutionCompatView, self).nav(active)
        return solution_compat_nav(self.node, self.category, nav, active)

    def get_node_list(self):
        return self.node.get_solutions(self.category)


provideAdapter(SolutionCompatView)
provideAdapter(SolutionCompatView, (ICompat, unicode))


class SolutionCompatUpdateView(UpdateView):
    adapts(ICompat)

    form = CompatNodeForm

provideAdapter(SolutionCompatUpdateView, name="update")


class AssignSolutionsView(UpdateView):
    adapts(ICompat, unicode)

    form = AssignSolutionsForm

    def __init__(self, node, category=None):
        super(AssignSolutionsView, self).__init__(node)
        # Use first category if not set, by default.
        if not category and node.categories:
            category = node.categories[0][0]
        self.category = category

    def get_form(self, *args, **kwargs):
        return self.form(self.category, self.node, *args, **kwargs)

    def nav(self, active=tuple()):
        if not active:
            if self.category:
                active = ('assign-solutions', self.category)
            else:
                active = ('assign-solutions',)
        nav = super(AssignSolutionsView, self).nav(active)
        return solution_compat_nav(self.node, self.category, nav, active)

provideAdapter(AssignSolutionsView, name='assign-solutions')


def match_mps_with_user(results, mps, user_vote):
    for name, mp_solution_vote in mps.items():
        if name not in results:
            results[name] = {'times': 0, 'sum': 0}
        results[name]['times'] += 1
        # If solutions will be weighted then then multiply with issue weight
        results[name]['sum'] += user_vote * mp_solution_vote

def sort_results(mps):
    return sorted(list([{
        'id': k,
        'times': v['times'],
        'score': int((1.0 * v['sum'] / v['times']) / 4 * 100),
    } for k, v in mps.items()]), key=lambda a: a['score'], reverse=True)


class QuickResultsView(NodeView):
    adapts(ISolution)

    def render(self):
        if self.request.GET.get('clean'):
            self.request.session['questions'] = []
            self.request.session['mps_matches'] = {}

        user_vote = self.request.GET.get('vote')
        if user_vote not in ('-2', '-1', '0', '1', '2'):
            raise Http404
        user_vote = int(user_vote)

        questions = self.request.session.get('questions', [])
        mps_matches = self.request.session.get('mps_matches', {})

        if self.node._id not in questions:
            # Save questions
            questions.append(self.node._id)
            self.request.session['questions'] = questions

            # Save mps
            mps_positions = self.node.mps_positions()
            match_mps_with_user(mps_matches, mps_positions, user_vote)
            self.request.session['mps_matches'] = mps_matches

        results = sort_results(mps_matches)
        if self.request.GET.get('raw'):
            return HttpResponse(
                '<table>' + ''.join(['''
                    <tr>
                        <td>%(id)s</td>
                        <td>x%(times)s</td>
                        <td>%(score)s%%</td>
                        <td><img src="%(url)s"> %(url)s</td>
                    </tr>''' % {
                        'id': a['id'],
                        'times': a['times'],
                        'score': a['score'],
                    } for a in results]) +
                '</table>')
        else:
            import json
            return HttpResponse(json.dumps({'mps': results[:8]}))

provideAdapter(QuickResultsView, name='quick-results')


class SolutionCompatJsonView(AjaxView):
    adapts(ISolution)

    def get_positions_list(self, positions):
        return [dict(
            position=position.position_percent(),
            avatar=position.profile.ref.avatar_url(),
            profile_url=position.profile.ref.permalink(),
            person=position.profile.ref.title,
        ) for position in positions]

    def render(self, **overrides):
        solution_id = self.node._id
        aye, against = PersonPosition.objects.mp_pairs(solution_id, limit=3)
        prefetch_nodes('profile', (aye, against))
        data = dict(
            mps_aye=self.get_positions_list(aye),
            mps_against=self.get_positions_list(against),
        )
        return json_response(data)

provideAdapter(SolutionCompatJsonView, name='compat')


class SolutionDetailsView(DetailsView):
    adapts(ISolution)

    template = 'votings/solution.html'

provideAdapter(SolutionDetailsView, name='compatibility')


class MPsPositionView(DetailsView):
    adapts(ISolution)
    template = 'solutions/mps_position.html'

    def nav(self, active=tuple()):
        active = active or ('seimo-pozicija')
        nav = super(MPsPositionView, self).nav(active)
        return solution_nav(self.node, nav, active)

    def render(self, **overrides):
        solution_id = self.node._id
        aye, against = PersonPosition.objects.mp_pairs(solution_id)
        context = {
            'positions': itertools.izip_longest(aye, against),
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
        return query_solution_votings(self.node._id)

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

                update_mps_positions(self.node._id)

                return redirect(self.node.permalink('balsavimai'))
        else:
            form = AssignVotingForm()

        context = {
            'form': form,
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
                update_mps_positions(self.node._id)
            return redirect(self.node.permalink('balsavimai'))
        else:
            raise Http404

provideAdapter(UnassignVotingView, name="delete")
