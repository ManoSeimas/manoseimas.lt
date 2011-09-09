from annoying.decorators import render_to

from manoseimas.models import Document

from .forms import SearchForm


@render_to('manoseimas/search/search_results.html')
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
        context['documents'] = Document.search(search)
        context['total_rows'] = context['documents'].total_rows

    return context
