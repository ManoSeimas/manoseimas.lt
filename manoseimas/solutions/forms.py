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

from sboard.forms import BaseNodeForm
from sboard.forms import NodeForm
from sboard.fields import NodeField


class SolutionForm(NodeForm):
    pass


class AssignIssueForm(BaseNodeForm):
    title = forms.CharField()
    summary = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea, required=False)


class SolutionIssueForm(BaseNodeForm):
    summary = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea, required=False)


class CounterArgumentForm(BaseNodeForm):
    parent = NodeField(required=True)
    summary = forms.CharField(widget=forms.Textarea)
    body = forms.CharField(widget=forms.Textarea, required=False)
