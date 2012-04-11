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


class SearchForm(forms.Form):
    number = forms.CharField(max_length=255)


class EditForm(forms.Form):
    summary = forms.CharField(widget=forms.widgets.Textarea(), required=False)
    proposed = forms.BooleanField(required=False)
    # TODO:albertas:2011-09-04: could not find max length of couchdb _id.
    doc_id = forms.CharField(max_length=255, widget=forms.HiddenInput())

    def __init__(self, document=None, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        if document and 'summary' in dict(document.items()):
            self.fields['summary'] = forms.CharField(initial=document['summary'],
                                                     widget=forms.widgets.Textarea())
        if document and 'proposed' in dict(document.items()):
            self.fields['proposed'] = forms.BooleanField(initial=document['proposed'])
