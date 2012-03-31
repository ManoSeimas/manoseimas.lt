from sboard.forms import NodeForm

from .models import PolicyIssue


class PolicyIssueForm(NodeForm):
    class Meta:
        document = PolicyIssue
        properties = ('title', 'parent', 'body')
