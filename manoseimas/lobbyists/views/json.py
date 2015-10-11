# -*- coding: utf-8 -*-

from django.http import JsonResponse

from manoseimas.lobbyists.models import Lobbyist


def _lobbyists_dict(lobbyist):
    return {
        'name': lobbyist.name,
        'slug': lobbyist.slug,
        'url': lobbyist.url,
        'company_code': lobbyist.company_code,
        'date_of_inclusion': lobbyist.date_of_inclusion,
        'law_project_count': lobbyist.law_project_count,
        'client_count': lobbyist.client_count,
        'avg_passed_law_project_ratio': 0,
    }

def lobbyists_json(request):
    lobbyists = Lobbyist.objects.all()
    return JsonResponse({'items': map(_lobbyists_dict, lobbyists),
                         'subtab_counts': _item_counts})


_item_counts = {'lobbyists': Lobbyist.objects.count(),
                'suggester_state': 111,
                'suggester_other': 7777}
