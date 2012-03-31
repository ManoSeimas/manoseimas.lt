from django.utils.translation import ugettext_lazy as _

from sboard.nodes import NodeView


class CategoryNode(NodeView):
    slug = 'categories'
    name = _('Category')
