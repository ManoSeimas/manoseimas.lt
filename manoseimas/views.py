import logging

from django.conf import settings
from django.shortcuts import render

from manoseimas.scrapy.models import Voting

logger = logging.getLogger(__name__)


def login(request):
    return render(request, 'manoseimas/login.html', {'settings': settings})


def votings(request):
    day = None
    recent = []
    last_date = ""
    for v in Voting.objects.order_by('-timestamp')[:100]:
        date = v.timestamp.date()
        if date != last_date:
            if len(recent) >= 7:
                break

            day = {'date': date, 'votings': []}
            recent.append(day)

        if not v.value['documents']:
            continue

        last_date = date
        title = v.get_title()

        if title is None:
            continue

        day['votings'].append({
            'id': v.key,
            'title': title,
            'date': v.timestamp
        })

    return render(request, 'votings.jade', {'recent_votings': recent})
