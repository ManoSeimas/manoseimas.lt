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

from django.shortcuts import render

from manoseimas.legal_acts.models import LegalAct

from .forms import SearchForm


def search_results(request):
    if 'query' in request.GET:
        search_form = SearchForm(data=request.GET)
        if search_form.is_valid():
            search = search_form.cleaned_data
    else:
        search_form = SearchForm()

    context = {
        'search_form': search_form,
    }
    if search:
        context['documents'] = LegalAct.search(search)
        context['total_rows'] = context['documents'].total_rows

    template = 'manoseimas/search/search_results.html'
    return render(request, template, context)
