from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.db.models import Prefetch

from couchdbkit.exceptions import ResourceNotFound

from sboard.models import couch

from manoseimas.compat.models import PersonPosition

from .models import (ParliamentMember, GroupMembership, Group,
                     StenogramStatement)


def mp_list(request, fraction_slug=None):
    def extract(mp):
        return {
            'id': mp.id,
            'full_name': mp.full_name,
            'slug': mp.slug,
            'photo_url': mp.photo.url,
            'fraction': (mp.current_fraction[0]
                         if mp.current_fraction else None),
        }

    def set_klass(fraction):
        fraction._klass = ('selected'
                           if fraction_slug == fraction.slug else None)
        return fraction

    fractions = map(set_klass, Group.objects.filter(type=Group.TYPE_FRACTION,
                                                    displayed=True))

    mps = ParliamentMember.objects.prefetch_related(
        Prefetch('groups',
                 queryset=Group.objects.filter(groupmembership__until=None,
                                               type=Group.TYPE_FRACTION,
                                               displayed=True),
                 to_attr='current_fraction')
    ).filter(groupmembership__until=None).distinct()

    if fraction_slug:
        fraction = Group.objects.get(
            type=Group.TYPE_FRACTION,
            slug=fraction_slug)
        mps = mps.filter(groups=fraction, groupmembership__until=None)

    mps_paginator = Paginator(mps, 24)
    mps_page_num = request.GET.get('page')
    try:
        mp_page = mps_paginator.page(mps_page_num)
    except PageNotAnInteger:
        mp_page = mps_paginator.page(1)
    except EmptyPage:
        mp_page = mps_paginator.page(mps_paginator.num_pages)

    mps = map(extract, mp_page.object_list)

    context = {
        'mps': mps,
        'mp_page': mp_page,
        'fractions': fractions,
        'all_klass': False if fraction_slug else 'selected'
    }

    return render(request, 'mp_catalog.jade', context)


def mp_fraction_list(request):
    fractions = Group.objects.filter(type=Group.TYPE_FRACTION)
    fractions = sorted(fractions, key=lambda f: f.active_member_count, reverse=True)
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
    mp_qs = ParliamentMember.objects.select_related('ranking', 'raised_by')

    mp_qs = mp_qs.prefetch_related(
        Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                until=None,
                group__type__in=(Group.TYPE_COMMITTEE,
                                 Group.TYPE_COMMISSION),
                group__displayed=True
            ),
            to_attr='committees'))
    mp_qs = mp_qs.prefetch_related(
        Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                until=None,
                group__type=Group.TYPE_GROUP,
                group__displayed=True),
            to_attr='other_groups'))
    mp_qs = mp_qs.prefetch_related(
        Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                until=None,
                group__type=Group.TYPE_FRACTION,
                group__displayed=True),
            to_attr='_fraction'))
    mp = mp_qs.get(slug=mp_slug)

    mp_qs = mp_qs.prefetch_related(
        Prefetch(
            'groupmembership',
            queryset=GroupMembership.objects.select_related('group').filter(
                group__type=Group.TYPE_FRACTION,
                group__displayed=True).order_by('-since'),
            to_attr='all_fractions'))
    mp = mp_qs.get(slug=mp_slug)

    profile = {'full_name': mp.full_name}
    if mp.fraction:
        profile["fraction_name"] = mp.fraction.name
        profile["fraction_slug"] = mp.fraction.slug
    else:
        profile["fraction_name"] = None

    profile['raised_by'] = mp.raised_by.name if mp.raised_by else None
    profile['office_address'] = mp.office_address
    profile['constituency'] = mp.constituency

    try:
        mp_node = couch.view('sboard/by_slug', key=mp.slug).one()
        positions = prepare_positions(mp_node)
    except ResourceNotFound:
        positions = None

    all_statements = StenogramStatement.objects.select_related(
        'topic').filter(speaker=mp).order_by('-topic__timestamp', '-pk')
    statement_paginator = Paginator(all_statements, 10)
    statement_page = request.GET.get('page')
    try:
        statements = statement_paginator.page(statement_page)
    except PageNotAnInteger:
        statements = statement_paginator.page(1)
    except EmptyPage:
        statements = statement_paginator.page(statement_paginator.num_pages)

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
        'groups': mp.other_groups,
        'all_fractions': mp.all_fractions,
        'committees': mp.committees,
        'biography': mark_safe(mp.biography),
        'stats': stats,
        'photo_url': mp.photo.url,
        'statements': statements,
        'ranking': mp.ranking,
    }

    return render(request, 'profile.jade', context)


def _statement_context(statement, highlighted=False):
    return {
        'id': statement.id,
        'speaker_id': statement.speaker.id if statement.speaker else None,
        'speaker_slug': statement.speaker.slug if statement.speaker else None,
        'speaker_name': statement.get_speaker_name(),
        'as_chairperson': statement.as_chairperson,
        'text': statement.text,
        'selected': highlighted,
    }


def _build_discussion_context(request, statement_id, selected_id=None):
    statement_qs = StenogramStatement.objects.select_related(
        'topic',
        'speaker').prefetch_related('topic__votings')
    statement = statement_qs.get(pk=statement_id)

    statements = statement.topic.statements.select_related('speaker').all()

    context = {
        'topic': {
            'id': statement.topic.id,
            'title': statement.topic.title,
            'timestamp': statement.topic.timestamp,
        },
        'selected_statement': _statement_context(statement),
        'statements': [
            _statement_context(stmt,
                               highlighted=(stmt.id == statement.id))
            for stmt in statements
        ],
    }
    return context


def mp_discussion(request, statement_id):
    context = _build_discussion_context(request, statement_id)
    return render(request, 'discussion.jade', context)


def mp_discussion_json(request, statement_id):
    context = _build_discussion_context(request, statement_id)
    return JsonResponse(context)
