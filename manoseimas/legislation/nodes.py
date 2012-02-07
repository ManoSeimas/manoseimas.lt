from django.conf.urls.defaults import patterns, url
from django.utils.translation import ugettext_lazy as _

from sboard.models import couch
from sboard.nodes import BaseNode

from .models  import Law, LawChange, LawProject


class LawNode(BaseNode):
    slug = 'legislation'
    name = _('Law')
    model = Law

    templates = {
        'details': 'legislation/law_details.html',
    }

    @classmethod
    def get_urls(cls):
        return patterns('sboard.views',
            url(r'^projects/$', 'node', {'view': 'law_projects'},
                name='law_projects'),

            url(r'^changes/$', 'node', {'view': 'law_changes'},
                name='law_changes'),
        )

    def get_law_projects(self):
        # TODO: rename legislation/drafts to sboard/by_key_and_type
        key = [self.node._id, 'LawProject']
        return couch.view('legislation/drafts', key=key)

    def get_law_changes(self):
        # TODO: rename legislation/drafts to sboard/by_key_and_type
        key = [self.node._id, 'LawChange']
        return couch.view('legislation/drafts', key=key)

    def law_projects_view(self, request):
        return self.list_view(request, {
            'get_node_list': self.get_law_projects,
            'template': 'legislation/law_list.html',
            'sidebar_template': 'legislation/sidebar/projects.html',
        })

    def law_changes_view(self, request):
        return self.list_view(request, {
            'get_node_list': self.get_law_changes,
            'template': 'legislation/law_list.html',
            'sidebar_template': 'legislation/sidebar/changes.html',
        })

    def details_view(self, request, overrides=None):
        return super(LawNode, self).details_view(request, {
            'sidebar_template': 'legislation/sidebar/law.html',
        })


class LawChangeNode(BaseNode):
    slug = 'legislation-changes'
    name = _('Law change')
    model = LawChange


class LawProjectNode(BaseNode):
    slug = 'legislation-projects'
    name = _('Law project')
    model = LawProject
