from django.shortcuts import render
from manoseimas.mps_v2.models import Group


def mp_fraction_list(request):
    fractions = Group.objects.filter(type=Group.TYPE_FRACTION)
    fractions = sorted(fractions, key=lambda f: f.active_member_count,
                       reverse=True)
    return render(request, 'fraction_list.jade', {'fractions': fractions})


def mp_fraction(request, fraction_slug):
    fraction = Group.objects.get(
        type=Group.TYPE_FRACTION,
        slug=fraction_slug
    )

    collaborating_fractions = fraction.top_collaborating_fractions
    members = fraction.active_members

    context = {
        'fraction': fraction,
        'members': members,
        'collaborating_fractions': collaborating_fractions,
        'positions': fraction.positions,
    }
    return render(request, 'fraction.jade', context)
