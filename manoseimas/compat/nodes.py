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
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from sboard.ajax import AjaxView
from sboard.nodes import DetailsView
from sboard.nodes import ListView
from sboard.nodes import NodeView
from sboard.nodes import UpdateView
from sboard.nodes import clone_view

from manoseimas.solutions.interfaces import ISolution

from .forms import AssignSolutionsForm
from .forms import CompatNodeForm
from .forms import UserPositionForm
from .interfaces import ICompat
from .models import mp_compatibilities_by_sign
from .models import fraction_compatibilities_by_sign
from .models import fetch_positions
from .models import query_positions
from .models import update_position


def solution_compat_nav(request, node, nav, active=tuple()):
    if node.can(request, 'update'):
        nav.append({
            'key': 'node-title',
            'title': _('Testas'),
            'header': True,
        })

        key = 'assign-solutions-categories'
        nav.append({
            'key': key,
            'url': node.permalink(key),
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
                'url': '#%s' % slug,
                'title': category['title'],
                'children': [],
                'active': slug in active,
            })

    return nav


TEST_BUTTONS = (
    (2, _(u'Tikrai už')),
    (1, _(u'Už')),
    (-1, _(u'Prieš')),
    (-2, _(u'Tikrai prieš')),
)


class SolutionCompatView(NodeView):
    adapts(ICompat)

    template = 'votings/question_group.html'

    def __init__(self, node):
        super(SolutionCompatView, self).__init__(node)

    def nav(self, active=tuple()):
        nav = super(SolutionCompatView, self).nav(active)
        return solution_compat_nav(self.request, self.node, nav, active)

    def get_category_list(self):
        for slug, category in self.node.categories:
            nodes = self.node.get_solutions(slug)
            yield {
                'slug': slug,
                'title': category['title'],
                'nodes': nodes,
                'positions': fetch_positions(self.request, nodes),
            }

    def render(self, **overrides):
        context = {
            'title': self.node.title,
            'view': self,
            'node': self.node,
            'buttons': TEST_BUTTONS,
            'categories': self.get_category_list(),
        }
        context.update(overrides)
        return render(self.request, self.template, context)

provideAdapter(SolutionCompatView)


class SolutionCompatUpdateView(UpdateView):
    adapts(ICompat)

    form = CompatNodeForm

provideAdapter(SolutionCompatUpdateView, name="update")


class AssignSolutionsCategoriesView(ListView):
    adapts(ICompat)

    def nav(self, active='assign-solutions-categories'):
        nav = super(AssignSolutionsCategoriesView, self).nav(active)
        return solution_compat_nav(self.request, self.node, nav, active)

    def get_node_list(self):
        for slug, cat in self.node.categories:
            yield {
                'title': cat['title'],
                'permalink': self.node.permalink(slug, 'assign-solutions'),
            }

    def render(self, **overrides):
        return super(AssignSolutionsCategoriesView, self).render(title=_(u'Pasirinkite kategoriją sprendimų priskyrimui'))

provideAdapter(AssignSolutionsCategoriesView, name='assign-solutions-categories')


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
        return solution_compat_nav(self.request, self.node, nav, active)

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


class SolutionCompatPreviewView(AjaxView):
    adapts(ISolution)

    def render(self, **overrides):
        solution_id = self.node._id
        aye, against = fraction_compatibilities_by_sign([(solution_id, self.position)], precise=True)
        return render(self.request, 'compat/compat_preview.html', {
            'aye': aye[:3],
            'against': against[:3],
        })


class UpdateUserPositionView(NodeView):
    adapts(ICompat)

    def render(self, **overrides):
        if self.request.method != 'POST':
            return HttpResponseBadRequest(_('Only POST requests are allowed.'))

        form = UserPositionForm(self.request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_text())

        solution = form.cleaned_data['node']
        position = form.cleaned_data['position']

        update_position(self.request, solution._id, position)
        view = clone_view(SolutionCompatPreviewView, self, solution)
        view.position = position
        return view.render()

provideAdapter(UpdateUserPositionView, name='submit-position')


class SolutionDetailsView(DetailsView):
    adapts(ISolution)

    template = 'votings/solution.html'

provideAdapter(SolutionDetailsView, name='compatibility')


class CompatResultsView(DetailsView):
    adapts(ICompat)
    template = 'compat/results.html'

    def nav(self, active=tuple()):
        return super(CompatResultsView, self).nav(active)

    def render(self, **overrides):
        positions = list(query_positions(self.request))
        mps = mp_compatibilities_by_sign(positions)
        fractions = fraction_compatibilities_by_sign(positions)
        context = {
            'groups': (
                {
                    'title': _('Frakcijos'),
                    'slug': 'frakcijos',
                    'compatibilities': list(map(list, itertools.izip_longest(*fractions))),
                },
                {
                    'title': _('Seimo nariai'),
                    'slug': 'seimo-nariai',
                    'compatibilities': itertools.izip_longest(*mps),
                },
            ),
            'title': _(u'Testo rezultatai'),
        }
        context.update(overrides)
        return super(CompatResultsView, self).render(**context)

provideAdapter(CompatResultsView, name='rezultatai')
