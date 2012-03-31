from zope.component import adapts
from zope.component import provideAdapter

from sboard.nodes import CreateView
from sboard.nodes import NodeView

from .forms import PolicyIssueForm
from .interfaces import IVoting
from .interfaces import IPolicyIssue


class VotingView(NodeView):
    adapts(IVoting)

    templates = {
        'details': 'votings/voting_details.html',
    }

provideAdapter(VotingView)


class CreatePolicyIssueView(CreateView):
    adapts(object, IPolicyIssue)

    form = PolicyIssueForm

provideAdapter(CreatePolicyIssueView, name="create")
