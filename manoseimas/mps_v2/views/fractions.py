# -*- coding: utf-8 -*-

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

    members = fraction.active_members.order_by('last_name')

    explanations = {
        'projects_collaboration': "",
        'stats_voitings': "Skaičiuojama, kokioje dalyje balsavimų frakcija dalyvavo (balsavo už, prieš arba susilaikė) nuo 2012 m. kadencijos pradžios. Frakcijos dalyvavimas balsavimuose skaičiuojamas pagal kiekvieno frakcijos nario dalyvavimą, apskaičiavus jų vidurkį.",
        'stats_discussions': "Skaičiuojama, kiek vidutiniškai kartų frakcijos narys pasisakė per Seimo plenarinius posėdžius nuo 2012 m. kadencijos pradžios.  Skaičiuojami visi pasisakymai.",
        'stats_long_statements': "Ilgi pasisakymai - daugiau nei 50 žodžių.",
        'stats_proposed_projects': "Skaičiuojama, kiek vidutiniškai kartų frakcijos narys pasirašė po Seimo narių teiktais teisės aktų projektais.",
        'stats_successful_projects': "Skaičiuojama, kiek vidutiniškai priimta frakcijos narių teikimui pasirašytų teisės aktų projektų.",
        'stats_projects_success_rate': "Skaičiuojama, kokia procentinė dalis frakcijos pateiktų teisės aktų projektų buvo priimti. Frakcijos priimtų projektų dalis skaičiuojama pagal kiekvieno frakcijos nario pateiktų ir priimtų teisės aktų projektų santykį, apskaičiavus jų vidurkį. Dėmesio!  Kokia dalis frakcijos pateiktų teisės aktų projektų bus priimti gali priklausyti nuo įvairių faktorių, pavyzdžiui, ar frakcija yra koalicijoje, ar opozicijoje.",
    }

    context = {
        'fraction': fraction,
        'members': members,
        'explanations': explanations,
    }
    return render(request, 'fraction.jade', context)
