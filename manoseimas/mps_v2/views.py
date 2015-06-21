from functools import partial
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.db.models import Prefetch, Count

from .models import (ParliamentMember, GroupMembership, Group,
                     Stenogram, StenogramStatement)


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
    mp_qs = mp_qs.prefetch_related(ParliamentMember.FractionPrefetch())
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
    profile['slug'] = mp_slug

    top_collaborators = mp.top_collaborators.prefetch_related(
        ParliamentMember.FractionPrefetch()
    )

    project_qs = mp.law_projects.order_by('-date')
    project_qs = project_qs.annotate(proposer_count=Count('proposers'))
    law_projects = [{
        'title': project.project_name,
        'date': project.date,
        'date_passed': project.date_passed,
        'number': project.project_number,
        'url': project.project_url,
        'proposer_count': project.proposer_count,

    } for project in project_qs[:10]]

    stats = {
        'statement_count': mp.statement_count,
        'long_statement_count': mp.long_statement_count,
        'long_statement_percentage': mp.get_long_statement_percentage,
        'contributed_discussion_percentage':
            mp.discussion_contribution_percentage,
        'votes': mp.votes,
        'vote_percent': mp.vote_percentage,
        'proposed_projects': mp.proposed_law_project_count,
        'passed_projects': mp.passed_law_project_count,
        'passed_project_percentage': mp.passed_law_project_ratio,
    }

    context = {
        'profile': profile,
        'positions': mp.positions,
        'groups': mp.other_groups,
        'all_fractions': mp.all_fractions,
        'committees': mp.committees,
        'biography': mark_safe(mp.biography),
        'stats': stats,
        'photo_url': mp.photo.url,
        'ranking': mp.ranking,
        'top_collaborating_mps': top_collaborators,
        'law_projects': law_projects,
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


def mp_statements(request, mp_slug, statement_page=None):
    mp = ParliamentMember.objects.get(slug=mp_slug)

    selected_session = request.GET.get('session')
    only_as_presenter = request.GET.get('only_as_presenter')
    sessions = Stenogram.objects.distinct().values_list('session', flat=True)

    all_statements = StenogramStatement.objects.select_related(
        'topic').filter(speaker=mp,
                        as_chairperson=False).order_by('-topic__timestamp',
                                                       '-pk')
    if selected_session:
        all_statements = all_statements.filter(
            topic__stenogram__session=selected_session)
    if only_as_presenter:
        all_statements = all_statements.filter(topic__presenters=mp)

    statement_paginator = Paginator(all_statements, 10)
    try:
        statements = statement_paginator.page(statement_page)
    except PageNotAnInteger:
        statements = statement_paginator.page(1)
    except EmptyPage:
        statements = statement_paginator.page(statement_paginator.num_pages)

    context = {
        'statements': statements,
        'sessions': sessions,
        'selected_session': selected_session
    }

    return render(request, 'statments.jade', context)


def index_view(request):
    return render(request, 'jsx.jade', {})


def _fraction_dict(fraction):
    return {
        'name': fraction.name,
        'slug': fraction.slug,
        'type': fraction.type,
        'logo_url': fraction.logo.url if fraction.logo else None,
        'url': reverse('mp_fraction', kwargs={'fraction_slug': fraction.slug}),
        'member_count': fraction.active_member_count,
        'avg_statement_count': int(fraction.avg_statement_count),
        'avg_long_statement_count': fraction.avg_long_statement_count,
        'avg_vote_percentage': int(fraction.avg_vote_percentage),
        'avg_discussion_contribution_percentage': fraction.avg_discussion_contribution_percentage,
        'avg_passed_law_project_ratio': int(fraction.avg_passed_law_project_ratio),
    }


def fractions_json(request):
    fractions = Group.objects.filter(type=Group.TYPE_FRACTION)
    fractions = filter(lambda f: bool(f.active_member_count), fractions)
    return JsonResponse({'items': map(_fraction_dict, fractions)})


def _mp_dict(mp, mp_fractions={}):
    data = {
        'first_name': mp['first_name'],
        'last_name': mp['last_name'],
        'full_name': ' '.join([mp['first_name'], mp['last_name']]),
        'slug': mp['slug'],
        'url': reverse('mp_profile', kwargs={'mp_slug': mp['slug']}),
        'photo': default_storage.url(mp['photo']),
        'statement_count': int(mp['statement_count']),
        'long_statement_count': mp['long_statement_count'],
        'vote_percentage': int(mp['vote_percentage']),
        'proposed_law_project_count': mp['proposed_law_project_count'],
        'passed_law_project_count': mp['passed_law_project_count'],
        'passed_law_project_ratio': int(mp['passed_law_project_ratio']),
    }
    fraction = mp_fractions.get(mp['pk'])
    if fraction:
        data.update({
            'fraction_name': fraction['name'],
            'fraction_url': reverse('mp_fraction', kwargs={
                'fraction_slug': fraction['slug']
            }),
        })
    return data


def mps_json(request):
    mps = ParliamentMember.objects.filter(
        groupmembership__until=None
    ).distinct().values('pk', 'first_name', 'last_name', 'slug',
                        'photo', 'statement_count', 'long_statement_count',
                        'vote_percentage', 'proposed_law_project_count',
                        'passed_law_project_count', 'passed_law_project_ratio')

    current_fractions = GroupMembership.objects.filter(
        group__type=Group.TYPE_FRACTION,
        until__isnull=True,
    ).select_related('group').values('member_id', 'group__name', 'group__slug')

    mp_fractions = {fraction['member_id']: {'name': fraction['group__name'],
                                            'slug': fraction['group__slug']}
                    for fraction in current_fractions}
    to_dict_partial = partial(_mp_dict, mp_fractions=mp_fractions)
    return JsonResponse({'items': map(to_dict_partial, mps)})
