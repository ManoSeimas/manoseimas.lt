from django import forms
from django.utils.translation import ugettext_lazy as _

from couchdbkit.ext.django.forms import DocumentForm

from sboard.forms import NodeForm

from .models import Solution
from .models import SolutionVoting


class SolutionForm(NodeForm):
    class Meta:
        document = Solution
        properties = ('title', 'parent', 'body')


class LinkSolutionForm(DocumentForm):
    solution = forms.SlugField()
    position = forms.BooleanField(initial=True, required=False,
            help_text=_('Uncheck if this voting is agains solution.'))
    weight = forms.IntegerField(initial=1)

    class Meta:
        document = SolutionVoting
        properties = ('solution', 'position', 'weight')
