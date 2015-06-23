from django.shortcuts import render

from manoseimas.mps_v2.models import Group

from .mps import *
from .fractions import *
from .statements import *
from .json import *


def index_view(request):
    parliament = Group.objects.get(type=Group.TYPE_PARLIAMENT)
    context = {'parliament': parliament}
    return render(request, 'index_with_filter.jade', context)
