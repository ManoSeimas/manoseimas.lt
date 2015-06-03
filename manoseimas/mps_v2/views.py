from django.shortcuts import render
from django.utils.safestring import mark_safe

from couchdbkit.exceptions import ResourceNotFound

from sboard.models import couch

from manoseimas.mps.nodes import prepare_position_list

from .models import ParliamentMember, GroupMembership, Group


def mp_list(request, fraction_slug=None):
    def extract(mp):
        return {
            'id': mp.id,
            'full_name': mp.full_name,
            'slug': mp.slug
        }

    fractions = Group.objects.filter(type=Group.TYPE_FRACTION)

    if fraction_slug:
        fraction = GroupMembership.objects.filter(
            group__type=Group.TYPE_FRACTION,
            group__slug=fraction_slug
        )
        fraction = fraction[0].group if fraction else None
        mps = map(extract, ParliamentMember.objects.filter(groups=fraction))
    else:
        mps = map(extract, ParliamentMember.objects.all())

    return render(request, 'mp_catalog.jade', {'mps': mps,
                                               'fractions': fractions})


def mp_profile(request, mp_slug):
    mp = ParliamentMember.objects.get(slug=mp_slug)

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

    stats = {
        'statement_count': mp.get_statement_count(),
        'long_statement_count': mp.get_long_statement_count(),
        'contributed_discussion_percentage':
            mp.get_discussion_contribution_percentage(),
    }

    context = {
        'profile': profile,
        'positions': positions,
        'memberships': mp.other_group_memberships,
        'biography': mark_safe(mp.biography),
        'stats': stats,
        'photo_url': mp.photo.url,
    }
    return render(request, 'profile.jade', context)
