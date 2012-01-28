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
