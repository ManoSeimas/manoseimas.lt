from django.utils.translation import ugettext_lazy as _

from sboard.nodes import BaseNode

from .models  import Law, LawChange, LawProject


class LawNode(BaseNode):
    slug = 'law'
    name = _('Law')
    model = Law


class LawChangeNode(BaseNode):
    slug = 'law-change'
    name = _('Law change')
    model = LawChange


class LawProjectNode(BaseNode):
    slug = 'law-project'
    name = _('Law project')
    model = LawProject
