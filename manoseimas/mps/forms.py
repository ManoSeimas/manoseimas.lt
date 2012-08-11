from django import forms

from sboard.forms import BaseNodeForm


class FractionForm(BaseNodeForm):
    title = forms.CharField()
    abbreviation = forms.CharField(required=False)
    image = forms.ImageField(required=False)

    def get_initial_values(self):
        initial = dict(self.node._doc)
        return initial

