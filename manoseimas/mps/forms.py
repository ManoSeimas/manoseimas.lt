# coding: utf-8
# Copyright (C) 2012  Mantas Zimnickas <sirexas@gmail.com>
#
# This file is part of manoseimas.lt project.
#
# manoseimas.lt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# manoseimas.lt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with manoseimas.lt.  If not, see <http://www.gnu.org/licenses/>.

from django import forms
from django.utils.translation import ugettext as _

from sboard.fields import NodeField
from sboard.forms import BaseNodeForm

from .models import Fraction


class FractionForm(BaseNodeForm):
    title = forms.CharField()
    abbreviation = forms.CharField(required=False)
    image = forms.ImageField(required=False)

    def get_initial_values(self):
        initial = dict(self.node._doc)
        return initial


class FractionMergeToForm(forms.Form):
    mergeto = NodeField(label=_(u'Sujungti su'),
        help_text=_(u'Nurodykite frakcijos slugą.'))

    def clean_mergeto(self):
        mergeto = self.cleaned_data.get('mergeto')
        if mergeto and not isinstance(mergeto, Fraction):
            raise forms.ValidationError(
                    _(u'Frakcijos, su tokiu nurodytu slugu nėra.'))
        return mergeto
