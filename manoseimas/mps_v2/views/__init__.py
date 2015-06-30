from django.shortcuts import render

from manoseimas.mps_v2.models import Group

from .mps import *
from .fractions import *
from .statements import *
from .json import *


def index_view(request):
    parliament = Group.objects.get(type=Group.TYPE_PARLIAMENT)
    explanations = {
      'votings': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                  sed do eiusmod tempor incididunt ut labore et dolore \
                  magna aliqua.",
      'statements': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                    sed do eiusmod tempor incididunt ut labore et dolore\
                    magna aliqua.',
      'projects': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                   sed do eiusmod tempor incididunt ut labore et dolore \
                   magna aliqua.'
    }
    context = {'parliament': parliament, 'explanations': explanations}
    return render(request, 'index_with_filter.jade', context)
