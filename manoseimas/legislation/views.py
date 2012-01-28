# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from couchdbkit.exceptions import ResourceNotFound


from .forms import SearchForm, EditForm

from manoseimas.pagination import CouchDbPaginator
from manoseimas.votings.models import Voting
from manoseimas.categories.models import Category

from .models import Law


def category_list(request):
    template = 'manoseimas/legislation/category_list.html'
    return render(request, template, {
        'categories': Category.get_tree(),
    })

def legislation_list(request):
    legislation = Law.view('legislation/by_name', include_docs=True)
    template = 'manoseimas/legislation/legislation_list.html'
    return render(request, template, {
        'legislations': CouchDbPaginator(legislation, request.GET),
    })

def legislation(request, legislation_id):
    template = 'manoseimas/legislation/legislation.html'
    try:
        category = Category.get(legislation_id)
        legislation = Law.view('legislation/by_category', limit=50,
                               startkey=[category.id],
                               endkey=[category.id, {}],
                               include_docs=True,)
    except ResourceNotFound:
        return render(request, template, {
            'legislation': Law.get(legislation_id),
        })
    else:
        return render(request, template, {
            'legislations': CouchDbPaginator(legislation, request.GET),
            'TEMPLATE': 'manoseimas/legislation/legislation_list.html',
        })




def document_search(request):
    document, edit_form, message = None, None, None
    search_form = SearchForm(data=request.POST or None)

    if request.POST and 'search' in request.POST and search_form.is_valid():
        key = search_form.cleaned_data['number']
        documents = Law.view('documents/by_number', limit=10,
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

    template = 'manoseimas/legislation/document_search.html'
    return render(request, template, {
        'search_form': search_form,
        'document': document,
        'edit_form': edit_form,
        'message': message,
    })


def legislation_amendments(request, legislation_id):
    template = 'manoseimas/legislation/amendments.html'
    return render(request, template, {
        'legislation': Law.get(legislation_id),
        'amendments': Law.view('legislation/amendments', limit=50,
                                     include_docs=True,
                                     startkey=[legislation_id, {}],
                                     endkey=[legislation_id],
                                     descending=True),
    })

def legislation_drafts(request, legislation_id):
    template = 'manoseimas/legislation/drafts.html'
    return render(request, template, {
        'legislation': Law.get(legislation_id),
        'drafts': Law.view('legislation/drafts', limit=50,
                                include_docs=True,
                                startkey=[legislation_id, {}],
                                endkey=[legislation_id],
                                descending=True),
    })

def legislation_all_drafts(request, legislation_id):
    template = 'manoseimas/legislation/drafts.html'
    return render(request, template, {
        'legislation': Law.get(legislation_id),
        'drafts': Law.view('legislation/drafts', limit=50,
                                include_docs=True,
                                startkey=[legislation_id, {}],
                                endkey=[legislation_id],
                                descending=True),
    })

def legislation_votings(request, legislation_id):
    template = 'manoseimas/legislation/votings.html'
    return render(request, template, {
        'legislation': Law.get(legislation_id),
        'votings': Voting.view('votings/parents', limit=25,
                               include_docs=True,
                               startkey=[legislation_id, {}],
                               endkey=[legislation_id],
                               descending=True),
    })
