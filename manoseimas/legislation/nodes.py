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
