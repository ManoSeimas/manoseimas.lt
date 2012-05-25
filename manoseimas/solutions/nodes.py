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

from zope.component import adapts
from zope.component import provideAdapter

from django.utils.translation import ugettext_lazy as _

from sboard.nodes import CreateView
from sboard.nodes import DetailsView

from .forms import SolutionForm
from .interfaces import ISolution


class SolutionDetailsView(DetailsView):
    adapts(ISolution)

    def nav(self, active=tuple()):
        if not active:
            active = ('index',)

        nav = super(SolutionDetailsView, self).nav(active)

        nav.append({
            'key': 'node-title',
            'title': _('Sprendimas'),
            'header': True,
        })

        key = 'index'
        nav.append({
            'key': key,
            'url': self.node.permalink(),
            'title': _('Sprendimas'),
            'children': [],
            'active': key in active,
        })

        return nav


provideAdapter(SolutionDetailsView)


class CreateSolutionView(CreateView):
    adapts(object, ISolution)

    form = SolutionForm

provideAdapter(CreateSolutionView, name="create")
