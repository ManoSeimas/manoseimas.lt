from django.utils.translation import ugettext_lazy as _

from sboard.nodes import BaseNode


class CategoryNode(BaseNode):
    slug = 'category'
    name = _('Category')
