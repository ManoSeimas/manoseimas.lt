from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.db.models import Prefetch

from couchdbkit.exceptions import ResourceNotFound

from sboard.models import couch

from manoseimas.compat.models import PersonPosition

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

    def set_klass(fraction):
        fraction._klass = 'selected' if fraction_slug == fraction.slug else None
        return fraction

    fractions = map(set_klass, Group.objects.filter(type=Group.TYPE_FRACTION))

    mps = ParliamentMember.objects.prefetch_related(
        Prefetch('groups',
                 queryset=Group.objects.filter(groupmembership__until=None,
                                               type=Group.TYPE_FRACTION),
                 to_attr='current_fraction')
    )

    if fraction_slug:
        fraction = Group.objects.get(
            type=Group.TYPE_FRACTION,
            slug=fraction_slug)
        mps = mps.filter(groups=fraction, groupmembership__until=None)

    mps = map(extract, mps)

    context = {
        'mps': mps,
        'fractions': fractions,
        'all_klass': False if fraction_slug else 'selected'
    }

    return render(request, 'mp_catalog.jade', context)


def mp_fraction_list(request):
    fractions = Group.objects.filter(type=Group.TYPE_FRACTION)
    return render(request, 'fraction_list.jade', {'fractions': fractions})


def prepare_positions(node):
    position_list = list(PersonPosition.objects.filter(profile=node))
    position_list.sort(key=lambda pp: abs(pp.position), reverse=True)

    positions = {'for': [], 'against': [], 'neutral': []}
    for position in position_list:
        if abs(position.position) < 0.2:
            positions['neutral'].append(position)
        elif position.position > 0:
            positions['for'].append(position)
        else:
            positions['against'].append(position)
    return positions


def mp_fraction(request, fraction_slug):
    fraction = Group.objects.get(
        type=Group.TYPE_FRACTION,
        slug=fraction_slug
    )

    members = fraction.members.filter(groupmembership__until=None)

    fraction_node = couch.view('sboard/by_slug', key=fraction.slug).one()

    positions = prepare_positions(fraction_node)
    context = {
        'fraction': fraction,
        'members': members,
        'positions': positions,
    }
    return render(request, 'fraction.jade', context)


def mp_profile(request, mp_slug):
    mp = ParliamentMember.objects.select_related('ranking').get(slug=mp_slug)

    profile = {'full_name': mp.full_name}
    if mp.fraction:
        profile["fraction_name"] = mp.fraction.name
        profile["fraction_slug"] = mp.fraction.slug
    else:
        profile["fraction_name"] = None

    try:
        mp_node = couch.view('sboard/by_slug', key=mp.slug).one()
        positions = prepare_positions(mp_node)
    except ResourceNotFound:
        positions = None

    stats = {
        'statement_count': mp.get_statement_count(),
        'long_statement_count': mp.get_long_statement_count(),
        'long_statement_percentage': mp.get_long_statement_percentage(),
        'contributed_discussion_percentage':
            mp.get_discussion_contribution_percentage(),
        'votes': mp.votes,
        'vote_percent': mp.get_vote_percentage(),
    }

    context = {
        'profile': profile,
        'positions': positions,
        'memberships': mp.other_group_memberships,
        'groups': mp.other_groups,
        'committees': mp.committees,
        'commissions': mp.commissions,
        'biography': mark_safe(mp.biography),
        'stats': stats,
        'photo_url': mp.photo.url,
        'statments': mp.all_statements,
        'ranking': mp.ranking,
    }

    import pdb; pdb.set_trace()
    return render(request, 'profile.jade', context)
