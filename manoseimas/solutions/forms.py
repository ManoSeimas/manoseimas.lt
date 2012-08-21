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
from django.utils.translation import ugettext_lazy as _

from sboard.forms import BaseNodeForm
from sboard.forms import NodeForm
from sboard.fields import NodeField

from manoseimas.votings.models import fetch_voting_by_lrslt_url
from manoseimas.votings.models import get_voting_by_source_id
from manoseimas.votings.models import get_voting_source_id_from_lrstl_url


class SolutionForm(NodeForm):
    pass


class AssignIssueForm(BaseNodeForm):
    title = forms.CharField()
    summary = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea, required=False)


class SolutionIssueForm(BaseNodeForm):
    summary = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea, required=False)
    listing_priority = forms.IntegerField(
        initial=0,
        label=_(u'Prioritetas sąrašuose'),
        help_text=_(u'Argumentai su aukštesniu prioritetu yra rodomi aukščiau.'))


class CounterArgumentForm(BaseNodeForm):
    parent = NodeField(required=True)
    summary = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea, required=False)


class AssignVotingForm(forms.Form):
    voting = forms.CharField(help_text=_(
        u'Nurodykite balsavimo adresą iš lrs.lt svetainės arba nurodykite '
        u'balsavimo ID iš manoseimas.lt svetainės.'))
    position = forms.IntegerField(initial=1, help_text=_(
        u'Iveskite sveiką saičių, kuris nurodo priskiriamo balsavimo svarbą. '
        u'Naudokite neigiamą reikšmę, jei balsuojama prieš šį sprendimą.'))

    def clean_voting(self):
        voting = self.cleaned_data.get('voting')
        if voting:
            node = None
            # Try voting as lrs.lt URL
            source_id = get_voting_source_id_from_lrstl_url(voting)
            if source_id:
                node = get_voting_by_source_id(source_id)
                if not node:
                    node = fetch_voting_by_lrslt_url(voting)
                if not node:
                    raise forms.ValidationError(_(
                        u'Klaidingai nurodytas balsavimo adresas lrs.lt '
                        u'svetainėje.'))
                return node
            else:
                raise forms.ValidationError(_(
                    u'Klaidingai nurodytas balsavimo adresas.'))
        return voting
