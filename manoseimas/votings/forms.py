from django import forms
from django.utils.translation import ugettext_lazy as _

from couchdbkit.ext.django.forms import DocumentForm

from sboard.forms import NodeForm

from .models import PolicyIssue
from .models import PolicyIssueLink


class PolicyIssueForm(NodeForm):
    class Meta:
        document = PolicyIssue
        properties = ('title', 'parent', 'body')


class LinkIssueForm(DocumentForm):
    solution = forms.SlugField()
    position = forms.BooleanField(initial=True, required=False,
            help_text=_('Uncheck if this voting is agains solution.'))
    weight = forms.IntegerField(initial=1)

    class Meta:
        document = PolicyIssueLink
        properties = ('solution', 'position', 'weight')
