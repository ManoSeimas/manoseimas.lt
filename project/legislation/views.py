from annoying.decorators import render_to

from mscouch.document import Document

from .forms import SearchForm, EditForm

import couchdb.design
couch = couchdb.Server('http://127.0.0.1:5984/')
db = couch['manoseimas']

# temporary sync
couchdb.design.ViewDefinition.sync_many(db, [
        Document.by_number,
    ])


@render_to('manoseimas/legislation/index.html')
def index(request):
    return {
        'documents': Document.by_number(db, limit=10),
    }


@render_to('manoseimas/legislation/search.html')
def search(request):
    documents = []
    search_form = SearchForm(data=request.POST or None)

    if request.POST and search_form.is_valid():
        key = search_form.cleaned_data['number']
        documents = Document.by_number(db, limit=10, include_docs=True)[key]

    return {
        'search_form': search_form,
        'documents': documents,
    }


@render_to('manoseimas/legislation/edit.html')
def edit(request, doc_id=None):
    message = None
    document = db[doc_id]
    edit_form = EditForm(document=document, data=request.POST or None)

    if request.POST and edit_form.is_valid():
        if document['doc_type'] == 'document':
            document['summary'] = edit_form.cleaned_data['summary']
            db.save(document)
            message = 'Successfully saved.'

    return {
        'edit_form': edit_form,
        'message': message,
    }
