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

from sboard.models import couch
from sboard.nodes import DetailsView
from sboard.nodes import ListView

from .interfaces import ILegalAct


class LawView(DetailsView):
    adapts(ILegalAct)

    templates = {
        'details': 'legislation/law_details.html',
    }

    def render(self, overrides=None):
        return super(LawView, self).render({
            'sidebar_template': 'legislation/sidebar/law.html',
        })

provideAdapter(LawView)


class ProjectsView(ListView):
    adapts(ILegalAct)

    def get_law_projects(self):
        return couch.view('legislation/projects',
                          startkey=[self.node._id, 'Z'],
                          endkey=[self.node._id], descending=True, limit=10)


    def render(self):
        return super(ProjectsView, self).render({
            'get_node_list': self.get_law_projects,
            'template': 'legislation/law_list.html',
            'sidebar_template': 'legislation/sidebar/projects.html',
        })

provideAdapter(ProjectsView, name='projects')


class ChangesView(ListView):
    adapts(ILegalAct)

    def get_law_changes(self):
        return couch.view('legislation/changes',
                          startkey=[self.node._id, 'Z'],
                          endkey=[self.node._id], descending=True, limit=10)

    def render(self):
        return super(ChangesView, self).render({
            'get_node_list': self.get_law_changes,
            'template': 'legislation/law_list.html',
            'sidebar_template': 'legislation/sidebar/changes.html',
        })

provideAdapter(ChangesView, name='changes')


class VotingsView(ListView):
    adapts(ILegalAct)

    def get_law_votings(self):
        return couch.view('votings/parents', startkey=[self.node._id, 'Z'],
                          endkey=[self.node._id], descending=True,
                          limit=10)

    def render(self):
        return super(VotingsView, self).render({
            'get_node_list': self.get_law_votings,
            'template': 'legislation/votings.html',
            'sidebar_template': 'legislation/sidebar/votings.html',
        })

provideAdapter(VotingsView, name='votings')
