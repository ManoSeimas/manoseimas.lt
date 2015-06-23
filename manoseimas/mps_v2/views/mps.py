from django.shortcuts import render
from django.db.models import Prefetch, Count
from django.utils.safestring import mark_safe

from manoseimas.mps_v2.models import (ParliamentMember, GroupMembership, Group, LawProject)


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

    project_qs = LawProject.objects.annotate(proposer_count=Count('proposers'))
    project_qs = project_qs.filter(proposers=mp)

    law_projects = [{
        'title': project.project_name,
        'date': project.date,
        'date_passed': project.date_passed,
        'number': project.project_number,
        'url': project.project_url,
        'proposer_count': project.proposer_count,
        'fraction_contributions': project.get_fraction_contributions(),
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
