from django.shortcuts import render

from couchdbkit.exceptions import ResourceNotFound

from sboard.models import couch

from manoseimas.mps.nodes import prepare_position_list

from .models import ParliamentMember, GroupMembership, Group


def mp_list(request, fraction_slug=None):
    def extract(mp):
        return {
            'id': mp.id,
            'full_name': mp.full_name
        }

    fractions = Group.objects.filter(type='fraction')

    if fraction_slug:
        selected_fraction = GroupMembership.objects.filter(group__type='fraction', group__slug=fraction_slug)
        if selected_fraction:
            selected_fraction = selected_fraction[0].group
        else:
            selected_fraction = None

        mps = map(extract, ParliamentMember.objects.filter(groups=selected_fraction))
    else:
        mps = map(extract, ParliamentMember.objects.all())

    return render(request, 'mp_catalog.jade', {'mps': mps, 'fractions': fractions})


def mp_profile(request, mp_id):
    mp = ParliamentMember.objects.get(id=mp_id)

    profile = {'full_name': mp.full_name}
    if mp.current_fraction:
        profile["fraction_name"] = mp.current_fraction.name
    else:
        profile["fraction_name"] = None

    try:
        mp_node = couch.get(mp.source_id)
        positions = prepare_position_list(mp_node)
    except ResourceNotFound:
        positions = None

    context = {
        'profile': profile,
        'positions': positions,
    }
    return render(request, 'profile.jade', context)

