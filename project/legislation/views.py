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
    document, edit_form = None, None
    search_form = SearchForm(data=request.POST or None)

    if request.POST and 'search' in request.POST and search_form.is_valid():
        key = search_form.cleaned_data['number']
        documents = Document.by_number(db, limit=10, include_docs=True)[key]
        document = documents.rows[0]
        edit_form = EditForm(document=documents.rows[0])
    elif request.POST and 'save' in request.POST:
        edit_form = EditForm(data=request.POST)
        if request.POST and edit_form.is_valid():
            document = db[edit_form.cleaned_data['doc_id']]
            if document['doc_type'] == 'document':
                document['summary'] = edit_form.cleaned_data['summary']
                db.save(document)

    return {
        'search_form': search_form,
        'document': document,
        'edit_form': edit_form,
    }
