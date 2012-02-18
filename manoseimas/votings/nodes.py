from django.utils.translation import ugettext_lazy as _

from sboard.nodes import BaseNode

from .models  import Voting


class VotingNode(BaseNode):
    slug = 'legislation-votings'
    name = _('Law voting')
    model = Voting
