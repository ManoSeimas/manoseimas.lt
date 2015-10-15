# -*-coding: utf-8 -*-

from django.shortcuts import render
from manoseimas.lobbyists.models import Lobbyist


def lobbyist_profile(request, lobbyist_slug):
    """A profile view for a lobbyist."""

    try:
        lobbyist = Lobbyist.objects.get(slug=lobbyist_slug)
    except Lobbyist.DoesNotExist:
        # TODO: handle this case gracefully
        lobbyist = None

    profile = {
        'name': lobbyist.name if lobbyist else 'Lobistas',
        'slug': lobbyist_slug
    }

    context = {
        'profile': profile,
    }

    return render(request, 'lobbyist_profile.jade', context)

