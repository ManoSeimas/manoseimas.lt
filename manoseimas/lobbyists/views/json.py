# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import JsonResponse

from manoseimas.lobbyists.models import Lobbyist


def _lobbyists_dict(lobbyist):
    return {
        'name': lobbyist.name,
        'slug': lobbyist.slug,
        'url': reverse('lobbyist_profile', kwargs={'lobbyist_slug': lobbyist.slug}),
        'company_code': lobbyist.company_code,
        'date_of_inclusion': lobbyist.date_of_inclusion,
        'law_project_count': lobbyist.law_project_count,
        'client_count': lobbyist.client_count,
        'avg_passed_law_project_ratio': 0, # TODO: remove or fill in this placeholder
    }

def lobbyists_json(request):
    lobbyists = Lobbyist.objects.all()
    return JsonResponse({'items': map(_lobbyists_dict, lobbyists),
                         'subtab_counts': subtab_counts()})


def _law_project_dict(project):
    return {
        'title': project.title,
        'client': project.client.name,
    }

def law_projects_json(request, lobbyist_slug):
    law_projects = {}
    lobbyist = Lobbyist.objects.get(slug=lobbyist_slug)
    projects = lobbyist.get_law_projects()
    return JsonResponse({'items': map(_law_project_dict, projects)})


def subtab_counts():
    """A copy from manoseimas/mps_v2/views/json.py. KEEP IN SYNC TIL REFACTORED."""
    return {'lobbyists': Lobbyist.objects.count(),
            'suggester_state': 111,  # Placeholder
            'suggester_other': 7777} # Placeholder
