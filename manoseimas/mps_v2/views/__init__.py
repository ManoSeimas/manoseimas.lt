# -*- coding: utf-8 -*-

from django.shortcuts import render

from manoseimas.mps_v2.models import Group

from .mps import *
from .fractions import *
from .statements import *
from .suggesters import *
from .json import *


def index_view(request):
    parliament = Group.objects.filter(type=Group.TYPE_PARLIAMENT).order_by('-name').first()
    explanations = {
        'votings': "Šis rodiklis parodo, kiek vidutiškai balsavimų Seimo narys dalyvavo nuo 2012 m. (balsavo už, prieš arba susilaikė).",
        'statements': "Šis rodiklis parodo, kiek vidutiniškai kartų nuo 2012 m. kadencijos pradžios Seimo narys pasisakė Seimo plenarinių posėdžių metu. Skaičiuojami visi pasisakymai.",
        'projects': 'Šis rodiklis parodo, kiek vidutiniškai kartų Seimo narys pasirašė po Seimo narių teiktais teisės aktų projektais.'
    }
    context = {'parliament': parliament, 'explanations': explanations}
    return render(request, 'index_with_filter.jade', context)
