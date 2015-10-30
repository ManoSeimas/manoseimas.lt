# -*-coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from manoseimas.mps_v2.models import Suggester


def suggester_profile(request, suggester_slug):
    """A profile view for a suggester."""

    suggester = get_object_or_404(Suggester.objects, slug=suggester_slug)

    profile = {
        'title': suggester.title if suggester else 'Suinteresuotas asmuo',
        'slug': suggester_slug,
    }

    context = {
        'profile': profile,
    }

    return render(request, 'suggester_profile.jade', context)

