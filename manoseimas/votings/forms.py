from django import forms
from django.utils.translation import ugettext_lazy as _

from sboard.forms import NodeForm

from .models import Solution


class SolutionForm(NodeForm):
    class Meta:
        document = Solution
        properties = ('title', 'parent', 'body')


class LinkSolutionForm(forms.Form):
    solution = forms.SlugField()
    position = forms.BooleanField(initial=True, required=False,
            help_text=_('Uncheck if this voting is agains solution.'))
    weight = forms.IntegerField(initial=1)
