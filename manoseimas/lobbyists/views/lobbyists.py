# -*-coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from manoseimas.lobbyists.models import Lobbyist


def lobbyist_profile(request, lobbyist_slug):
    """A profile view for a lobbyist."""

    lobbyist = get_object_or_404(Lobbyist.objects, slug=lobbyist_slug)

    profile = {
        'name': lobbyist.name if lobbyist else 'Lobistas',
        'slug': lobbyist_slug
    }

    context = {
        'profile': profile,
    }

    return render(request, 'lobbyist_profile.jade', context)

