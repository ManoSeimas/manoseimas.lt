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

from zope.component import adapts
from zope.component import provideAdapter

from django import forms
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from sboard.models import couch

from manoseimas.votings.interfaces import IVoting
from manoseimas.votings.nodes import VotingView


class LinkSolutionForm(forms.Form):
    solution = forms.SlugField()
    position = forms.IntegerField(initial=1,
            help_text=_('Use negative value if this voting is against '
                        'solution.'))

    def clean_solution(self):
        solution = self.cleaned_data.get('solution')
        if solution:
            return couch.by_slug(key=solution).one(True)
        else:
            return solution


class MsVotingView(VotingView):
    form = LinkSolutionForm

    def get_solutions(self):
        return couch.view('votings/solutions_by_voting', key=self.node._id)

    def render(self, **overrides):
        context = {
            'solutions': self.get_solutions(),
        }
        context.update(overrides)

        if 'link_solution_form' not in context:
            context['link_solution_form'] = LinkSolutionForm()

        return super(MsVotingView, self).render(**context)

provideAdapter(MsVotingView)


class LinkSolutionView(MsVotingView):
    adapts(IVoting)

    def render(self):
        if self.request.method == 'POST':
            if not self.can('update', None):
                return render(self.request, '403.html', status=403)

            form = self.form(self.request.POST)
            if form.is_valid():
                if 'solutions' not in self.node:
                    self.node.solutions = {}
                solution = form.cleaned_data.pop('solution')
                position = form.cleaned_data.pop('position')
                self.node.solutions[solution._id] = position
                self.node.save()
                return redirect(self.node.permalink())
        else:
            form = self.get_form()

        return super(LinkSolutionView, self).render(link_solution_form=form)

provideAdapter(LinkSolutionView, name="link-solution")
