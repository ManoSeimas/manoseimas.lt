
# -*- coding: utf-8 -*-
#
# Views that display lobbyists

from django.shortcuts import render


def lobbyist_list_view(request):
    """List lobbyists."""
    lobbyists = Lobbyist.objects.filter.all()
    return render(request, 'lobbyist_list.jade', {'lobbyists': lobbyists})

