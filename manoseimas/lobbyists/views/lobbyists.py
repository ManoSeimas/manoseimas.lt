# -*-coding: utf-8 -*-

from django.shortcuts import render
from manoseimas.lobbyists.models import Lobbyist

def lobbyist_list(request):
    """A placeholder."""
    lobbyists = Lobbyist.objects.all()
    return render(request, 'lobbyist_list.jade', {lobbyists: lobbyists})


def lobbyist_profile(request, lobbyist_slug):
    """A profile view for a lobbyist."""

    try:
        lobbyist = Lobbyist.objects.get(slug=lobbyist_slug)
    except Lobbyist.DoesNotExist:
        lobbyist = None

    profile = {
        'name': lobbyist.name if lobbyist else 'Lobistas',
        'slug': lobbyist_slug
    }

    context = {
        'profile': profile,
    }

    return render(request, 'lobbyist_profile.jade', context)

