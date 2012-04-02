from zope.component import adapts
from zope.component import provideAdapter

from sboard.models import couch
from sboard.nodes import DetailsView
from sboard.nodes import ListView

from .interfaces import ILawChange
from .interfaces import ILawProject
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
        # TODO: rename legislation/drafts to sboard/by_key_and_type
        key = [self.node._id, 'LawProject']
        return couch.view('legislation/drafts', key=key)

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
        # TODO: rename legislation/drafts to sboard/by_key_and_type
        key = [self.node._id, 'LawChange']
        return couch.view('legislation/drafts', key=key)

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


class LawChangeNode(LawView):
    adapts(ILawChange)

provideAdapter(VotingsView)


class LawProjectNode(LawView):
    adapts(ILawProject)

provideAdapter(VotingsView)
