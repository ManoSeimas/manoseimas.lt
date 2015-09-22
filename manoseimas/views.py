import unidecode
from django.shortcuts import render
from decorators import ajax_request

from manoseimas.votings.models import get_recent_votings

from sboard.nodes import search_words_re
from sboard.models import couch

import logging

logger = logging.getLogger(__name__)


def votings(request):
    day = None
    recent = []
    last_date = ""
    for v in get_recent_votings(100):
        date = v.created.date()
        if date != last_date:
            if len(recent) >= 7:
                break

            day = {'date': date, 'votings': []}
            recent.append(day)

        last_date = date
        title = v.documents[0]['name'] if v.documents else v.title

        day['votings'].append({
            'id': v._id,
            'title': title,
            'date': v.created
        })

    return render(request, 'votings.jade', {'recent_votings': recent})


def normalize_search(value):
    r = unidecode.unidecode(value)
    return r.lower()


@ajax_request('GET')
def ajax_search(request):
    qry = normalize_search(request.GET.get('q'))
    qry = search_words_re.split(qry)
    qry = filter(None, qry)
    if len(qry):
        key = qry[0]
        args = dict(startkey=[key, 'Z'], endkey=[key])
        nodes = couch.view('compat/search', descending=True, limit=25, **args)
        results = []
        for n in nodes:
            r = {'id': n._id, 'type': n.doc_type}
            if 'title' in n:
                r['title'] = n.title
            if 'created' in n:
                r['created'] = str(n.created)
            if n.doc_type == "Voting":
                docs = []
                for doc in n.documents:
                    if key in normalize_search(doc['name']):
                        docs.append(doc)

                r['documents'] = docs

            results.append(r)
        return results

    else:
        return []

