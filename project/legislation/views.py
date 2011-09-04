from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from annoying.decorators import render_to

from mscouch.document import Document

from .forms import SearchForm, EditForm

import couchdb.design
couch = couchdb.Server('https://manoseimas:politika@manoseimas.cloudant.com')
db = couch['manoseimas']

# temporary sync
couchdb.design.ViewDefinition.sync_many(db, [
        Document.by_number,
        Document.proposed_only,
    ])


@render_to('manoseimas/legislation/document_list.html')
def document_list(request):
    return {
        'documents': Document.proposed_only(db, limit=10),
    }


@render_to('manoseimas/legislation/document_search.html')
def document_search(request):
    document, edit_form, message = None, None, None
    search_form = SearchForm(data=request.POST or None)

    if request.POST and 'search' in request.POST and search_form.is_valid():
        key = search_form.cleaned_data['number']
        documents = Document.by_number(db, limit=10, include_docs=True)[key]
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
            return HttpResponseRedirect(reverse('manoseimas-legislation-document-list'))

    return {
        'search_form': search_form,
        'document': document,
        'edit_form': edit_form,
        'message': message,
    }


@render_to('manoseimas/legislation/legislation.html')
def legislation(request, legislation_id):
    document = db[legislation_id]
    if document['doc_type'] != 'document':
        return {}

    lrs_url = 'http://www3.lrs.lt/pls/inter3/dokpaieska.showdoc_l?p_id=403303'

    return {
        'document': document,
        'lrs_url': lrs_url,
    }
