# coding: utf-8

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from annoying.decorators import render_to

from .forms import SearchForm, EditForm

from manoseimas.models import Document
from manoseimas.pagination import CouchDbPaginator


@render_to('manoseimas/legislation/legislation_list.html')
def legislation_list(request):
    legislations = Document.view('legislation/by_name', include_docs=True)
    return {
        'legislations': CouchDbPaginator(legislations, request.GET),
    }


@render_to('manoseimas/legislation/document_search.html')
def document_search(request):
    document, edit_form, message = None, None, None
    search_form = SearchForm(data=request.POST or None)

    if request.POST and 'search' in request.POST and search_form.is_valid():
        key = search_form.cleaned_data['number']
        documents = Document.view('documents/by_number', limit=10,
                                  include_docs=True)[key]
        if len(documents):
            document = documents.rows[0]
            edit_form = EditForm(document=documents.rows[0])
        else:
            message = "No result found."
    elif request.POST and 'save' in request.POST:
        edit_form = EditForm(data=request.POST)
        key = edit_form.data['doc_id']
        document = db[key]
        if request.POST and edit_form.is_valid():
            if document['doc_type'] == 'document':
                document['summary'] = edit_form.cleaned_data['summary']
                document['proposed'] = edit_form.cleaned_data['proposed']
                db.save(document)
            return HttpResponseRedirect(reverse('manoseimas-legislation-list'))

    return {
        'search_form': search_form,
        'document': document,
        'edit_form': edit_form,
        'message': message,
    }


@render_to('manoseimas/legislation/legislation.html')
def legislation(request, legislation_id):
    return {
        'legislation': Document.get(legislation_id),
    }

@render_to('manoseimas/legislation/amendments.html')
def legislation_amendments(request, legislation_id):
    return {
        'legislation': Document.get(legislation_id),
        'amendments': Document.view('legislation/amendments', limit=50,
                                     include_docs=True,
                                     startkey=[legislation_id],
                                     endkey=[legislation_id,'Z']),
    }

@render_to('manoseimas/legislation/drafts.html')
def legislation_drafts(request, legislation_id):
    return {
        'legislation': Document.get(legislation_id),
        'drafts': Document.view('legislation/drafts', limit=50,
                                include_docs=True,
                                startkey=[legislation_id],
                                endkey=[legislation_id,'Z']),
    }
