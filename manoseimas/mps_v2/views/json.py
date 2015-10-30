# -*- coding: utf-8 -*-

import re

from functools import partial

from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.db.models import Count

from manoseimas.mps_v2.models import (CommitteeResolution,
                                      Group,
                                      GroupMembership,
                                      LawProject,
                                      ParliamentMember,
                                      Suggestion)
from manoseimas.utils import round

from .statements import _build_discussion_context


def mp_discussion_json(request, statement_id):
    context = _build_discussion_context(request, statement_id)
    return JsonResponse(context)


def _fraction_dict(fraction):
    default_logo = '/static/img/fractions/fraction-default.png'
    return {
        'name': fraction.name,
        'slug': fraction.slug,
        'type': fraction.type,
        'logo_url': fraction.logo.url if fraction.logo else default_logo,
        'url': reverse('mp_fraction', kwargs={'fraction_slug': fraction.slug}),
        'member_count': fraction.active_member_count,
        'avg_statement_count': round(fraction.avg_statement_count),
        'avg_long_statement_count': fraction.avg_long_statement_count,
        'avg_vote_percentage': round(fraction.avg_vote_percentage),
        'avg_discussion_contribution_percentage':
            fraction.avg_discussion_contribution_percentage,
        'avg_passed_law_project_ratio':
            round(fraction.avg_passed_law_project_ratio),
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
        'vote_percentage': round(mp['vote_percentage']),
        'proposed_law_project_count': mp['proposed_law_project_count'],
        'passed_law_project_count': mp['passed_law_project_count'],
        'passed_law_project_ratio': round(mp['passed_law_project_ratio']),
    }
    fraction = mp_fractions.get(mp['pk'])
    if fraction:
        data.update({
            'fraction_name': fraction['name'],
            'fraction_url': reverse('mp_fraction', kwargs={
                'fraction_slug': fraction['slug']
            }),
            'fraction_slug': fraction['slug'],
            'fraction_logo_url': default_storage.url(fraction['logo']),
        })
    return data


def mps_json(request, fraction_slug=None):
    mp_qs = ParliamentMember.objects.filter(
        groupmembership__until=None,
        groupmembership__group__type=Group.TYPE_FRACTION,
    )
    if fraction_slug:
        mp_qs = mp_qs.filter(groupmembership__group__slug=fraction_slug,
                             groupmembership__until__isnull=True)
    mps = mp_qs.distinct().values('pk', 'first_name', 'last_name', 'slug',
                                  'photo', 'statement_count',
                                  'long_statement_count', 'vote_percentage',
                                  'proposed_law_project_count',
                                  'passed_law_project_count',
                                  'passed_law_project_ratio')

    current_fractions = GroupMembership.objects.filter(
        group__type=Group.TYPE_FRACTION,
        until__isnull=True,
    ).select_related('group').values('member_id', 'group__name', 'group__slug',
                                     'group__logo')

    mp_fractions = {fraction['member_id']: {'name': fraction['group__name'],
                                            'slug': fraction['group__slug'],
                                            'logo': fraction['group__logo']}
                    for fraction in current_fractions}
    to_dict_partial = partial(_mp_dict, mp_fractions=mp_fractions)
    return JsonResponse({'items': map(to_dict_partial, mps)})


def law_projects_json(request, mp_slug):
    def make_dict(fraction):
        return {
            'name': fraction.name,
            'slug': fraction.slug,
            'type': fraction.type,
            'url': reverse('mp_fraction',
                           kwargs={'fraction_slug': fraction.slug}),
            'contribution': fraction.fraction_contribution,
        }

    mp = ParliamentMember.objects.get(slug=mp_slug)

    project_qs = LawProject.objects.annotate(proposer_count=Count('proposers'))
    project_qs = project_qs.filter(proposers=mp)

    law_projects = [{
        'title': project.project_name,
        'date': project.date,
        'date_passed': project.date_passed,
        'number': project.project_number,
        'url': project.project_url,
        'proposer_count': project.proposer_count,
    } for project in project_qs]

    return JsonResponse({'items': law_projects})

def suggesters_json(request):
    state_actor_filter = request.GET.get('state_actor', '').lower()
    if state_actor_filter in ('0', 'false', 'no'):
        suggesters = Suggestion.suggestion_and_project_count_other()
    elif state_actor_filter in ('1', 'true', 'yes'):
        suggesters = Suggestion.suggestion_and_project_count_state()
    else:
        suggesters = Suggestion.suggestion_and_project_count()
    return JsonResponse({'items': suggesters,
                         'subtab_counts': subtab_counts()})


def _mangle(text):
    text = re.sub(u'^\s*(PAGRINDINIO )?(KOMITETO )?(IŠVADA )?\s*', u'', text)
    return text

def _resolution_dict(resolution):
    return {
        'title': _mangle(resolution.title),
        'url': resolution.source,
    }

def resolutions_json(request, suggester_slug):
    """Get resolutions for a given suggester."""
    resolutions_qs = CommitteeResolution.objects.filter(
        suggestion__submitter__slug=suggester_slug).distinct()

    return JsonResponse({'items': map(_resolution_dict, resolutions_qs)})


# TODO: this needs refactoring BADLY. We risk circular imports.
from manoseimas.lobbyists.models import Lobbyist
def subtab_counts():
    """Counts of 'actors' in each subtab."""
    return {'lobbyists': Lobbyist.objects.count(),
            'suggester_state': len(Suggestion.suggestion_and_project_count_state()),
            'suggester_other': len(Suggestion.suggestion_and_project_count_other()),
            }
