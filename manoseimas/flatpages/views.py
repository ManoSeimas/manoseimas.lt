from django.shortcuts import render
from django.http import Http404
from .models import FlatPage


def flatpage_view(request, page):
    try:
        flatpage = FlatPage.objects.get(name=page)
    except FlatPage.DoesNotExist:
        raise Http404

    return render(request, 'flatpage/page.jade', {'title': flatpage.title,
                                                  'content': flatpage.content})
