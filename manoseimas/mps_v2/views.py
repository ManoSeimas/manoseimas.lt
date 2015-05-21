from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render

from couchdbkit.exceptions import ResourceNotFound

from sboard.models import couch

from manoseimas.mps.nodes import prepare_position_list

from .models import ParliamentMember


def mp_list(request):
    mps = ParliamentMember.objects.all()
    mp_links = [u'<a href="{}">{}</a>'.format(reverse('mp_profile',
                                                      args=[mp.id]),
                                              mp.full_name)
                for mp in mps]
    return HttpResponse(u'<br/>'.join(mp_links))


def mp_profile(request, mp_id):
    mp = ParliamentMember.objects.get(id=mp_id)
    fraction = mp.fraction
    profile = {
        'full_name': mp.full_name,
        'fraction': fraction.name,
    }

    try:
        mp_node = couch.get(mp.source_id)
        positions = prepare_position_list(mp_node)
    except ResourceNotFound:
        positions = None

    context = {
        'profile': profile,
        'positions': positions,
    }
    return render(request, 'mps_v2/profile.html', context)
