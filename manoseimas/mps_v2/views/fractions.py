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
    members = fraction.active_members.order_by('last_name')

    explanations = {
        'projects_collaboration': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                  sed do eiusmod tempor incididunt ut labore et dolore \
                  magna aliqua.",
        'stats_voitings': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                  sed do eiusmod tempor incididunt ut labore et dolore \
                  magna aliqua.",
        'stats_discussions': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                  sed do eiusmod tempor incididunt ut labore et dolore \
                  magna aliqua.",
        'stats_long_statements': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                  sed do eiusmod tempor incididunt ut labore et dolore \
                  magna aliqua.",
        'stats_proposed_projects': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                  sed do eiusmod tempor incididunt ut labore et dolore \
                  magna aliqua.",
        'stats_projects_success_rate': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, \
                  sed do eiusmod tempor incididunt ut labore et dolore \
                  magna aliqua.",
    }

    context = {
        'fraction': fraction,
        'members': members,
        'collaborating_fractions': collaborating_fractions,
        'positions': fraction.positions,
        'explanations': explanations,
    }
    return render(request, 'fraction.jade', context)
