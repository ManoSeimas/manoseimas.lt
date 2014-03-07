from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from django.shortcuts import render

from manoseimas.votings.models import get_recent_votings

import logging
logger = logging.getLogger(__name__)

def index(request):
    day = None
    recent = []
    last_date = "";
    for v in get_recent_votings(100):
        date = v.created.date()
        if date != last_date:
            if len(recent) >= 7:
                break

            day = { 'date': date, 'votings': [] }
            recent.append(day)

        last_date = date
        title = v.documents[0]['name'] if v.documents else v.title

        day['votings'].append({
            'id': v._id,
            'title': title,
            'date': v.created
        })

    params = { 
        'recent_votings': recent
    }
    return render(request, 'index.html', params)

