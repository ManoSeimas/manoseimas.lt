from django.utils.translation import ugettext_lazy as _

from sboard.nodes import BaseNode

from .models  import Law, LawChange, LawProject


class LawNode(BaseNode):
    slug = 'legislation'
    name = _('Law')
    model = Law


class LawChangeNode(BaseNode):
    slug = 'legislation-changes'
    name = _('Law change')
    model = LawChange


class LawProjectNode(BaseNode):
    slug = 'legislation-projects'
    name = _('Law project')
    model = LawProject
