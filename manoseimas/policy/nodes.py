from django.utils.translation import ugettext_lazy as _

from sboard.nodes import NodeView


class PolicyNode(NodeView):
    slug = 'policies'
    name = _('Policy')
