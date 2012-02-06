from django.utils.translation import ugettext_lazy as _

from sboard.nodes import BaseNode


class PolicyNode(BaseNode):
    slug = 'policies'
    name = _('Policy')
