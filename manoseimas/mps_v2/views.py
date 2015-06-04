from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.db.models import Prefetch

from couchdbkit.exceptions import ResourceNotFound

from sboard.models import couch

from manoseimas.mps.nodes import prepare_position_list

from .models import ParliamentMember, GroupMembership, Group


def mp_list(request, fraction_slug=None):
    def extract(mp):
        return {
            'id': mp.id,
            'full_name': mp.full_name,
            'slug': mp.slug,
            'photo_url': mp.photo.url,
            'fraction': mp.current_fraction[0] if mp.current_fraction else None,
        }

    fractions = Group.objects.filter(type=Group.TYPE_FRACTION)

    mps = ParliamentMember.objects.prefetch_related(
        Prefetch('groups',
                 queryset=Group.objects.filter(groupmembership__until=None,
                    type=Group.TYPE_FRACTION),
                 to_attr='current_fraction')
    ).all()

    if fraction_slug:
        fraction = GroupMembership.objects.get(
            group__type=Group.TYPE_FRACTION,
            group__slug=fraction_slug
        )
        mps = mps.filter(groups=fraction, groupmembership__until=None)

    mps = map(extract, mps)

    return render(request, 'mp_catalog.jade', {'mps': mps,
                                               'fractions': fractions})


def mp_fraction(request, fraction_slug):
    pass

def mp_fraction_list(request):
    pass

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
        'votes': mp.votes
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
