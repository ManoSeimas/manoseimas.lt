from zope.component import adapts
from zope.component import provideAdapter

from sboard.interfaces import INode
from sboard.nodes import NodeView


class VotingView(NodeView):
    adapts(INode)

    slug = 'legislation-votings'

    templates = {
        'details': 'votings/voting_details.html',
    }

provideAdapter(VotingView, name="details")
