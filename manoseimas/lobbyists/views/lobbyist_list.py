# -*-coding: utf-8 -*-

from django.shortcuts import render
from manoseimas.lobbyists.models import Lobbyist

def lobbyist_list(request):
    lobbyists = Lobbyist.objects.all()
    return render(request, 'lobbyist_list.jade', {lobbyists: lobbyists})
