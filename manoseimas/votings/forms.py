from django import forms

from couchdbkit.ext.django.forms import DocumentForm

from sboard.forms import NodeForm

from .models import PolicyIssue
from .models import PolicyIssueLink


class PolicyIssueForm(NodeForm):
    class Meta:
        document = PolicyIssue
        properties = ('title', 'parent', 'body')


class LinkIssueForm(DocumentForm):
    policy_issue = forms.SlugField()
    vote_aye = forms.IntegerField()
    vote_no = forms.IntegerField()
    vote_abstain = forms.IntegerField()

    class Meta:
        document = PolicyIssueLink
        properties = ('policy_issue', 'vote_aye', 'vote_no', 'vote_abstain')
