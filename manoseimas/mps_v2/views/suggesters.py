# -*-coding: utf-8 -*-

from django.shortcuts import render
from manoseimas.mps_v2.models import Suggester


def suggester_profile(request, suggester_slug):
    """A profile view for a suggester."""

    try:
        suggester = Suggester.objects.get(slug=suggester_slug)
    except Suggester.DoesNotExist:
        # TODO: handle this case gracefully
        suggester = None

    profile = {
        'title': suggester.title if suggester else 'Suinteresuotas asmuo',
        'slug': suggester_slug,
    }

    context = {
        'profile': profile,
    }

    return render(request, 'suggester_profile.jade', context)

