# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from manoseimas.compatibility_test.models import CompatTest
from manoseimas.compatibility_test.models import Topic


def get_current_test():
    return CompatTest.objects.first()


def topics_all():
    qs = Topic.objects.all()
    test = get_current_test()
    qs = qs.filter(groups__test=test)
    qs = qs.prefetch_related('groups', 'arguments')

    topics = []
    for topic in qs:
        arguments = topic.arguments.all().values(
            'id', 'name', 'description', 'supporting'
        )
        topic_votings = topic.topicvoting_set.all().values(
            'voting__id', 'voting__name', 'voting__source', 'factor',
        )
        votings = [
            {
                'id': tv['voting__id'],
                'name': tv['voting__name'],
                'url': tv['voting__source'],
                'factor': tv['factor'],
            }
            for tv in topic_votings
        ]
        topics.append({
            'id': topic.id,
            'name': topic.name,
            'group': topic.groups.first().name,
            'description': topic.description,
            'arguments': list(arguments),
            'votings': votings,
        })
    # TODO: randomise by group #153
    return topics


class IndexView(View):
    template_name = 'start_test.jade'

    def topics(self):
        return [
            {
                "id": 1,
                "group": "Energetika",
                "name": "Aukštojo mokslo reforma",
                "description": 'Ar pritariate aukštojo mokslo reformai, įvedusiai "krepšelių" finansavimą, pakeitusiai aukštųjų mokyklų valdymą ir kt.?',
                "arguments": [
                    {
                        "id": 1,
                        "name": "Efektyvesnė veikla",
                        "description": "Reforma skatina aukštųjų mokyklų jungimąsi, didina jų konkurencingumą, studijų ir mokslo potencialą.",
                        "supporting": True,
                    }, {
                        "id": 2,
                        "name": "Gerinamas įvaizdis, o ne studijų kokybė",
                        "description": "Šiuo metu sunku vertinti ir rinktis studijų programas pagal jų kokybę, todėl aukštosios mokyklos vilioja studentus 'fasadiniais' pokyčiais.",
                        "supporting": False,
                    }, {
                        "id": 3,
                        "name": "Aukštesnė studijų kokybė",
                        "description": "Reforma siekia kelti aukštojo mokslo kokybę Lietuvoje ir panaikinti prastos kokybės studijų programas.",
                        "supporting": True,
                    },
                ]
            }, {
                "id": 2,
                "group": "Energetika",
                "name": "Visagino atominė elektrinė",
                "description": 'Ar pritariate Visagino atominės elektrinės statybai Lietuvoje?',
                "arguments": [
                    {
                        "id": 4,
                        "name": "Tikslingai formuojamos studijų kryptys",
                        "description": "Tikslingu valstybės finansavimu skatinamos darbo rinkoje paklausios studijų kryptys ir mažinamas perteklinių studijų krypčių patrauklumas.",
                        "supporting": True,
                    }, {
                        "id": 5,
                        "name": "Priimami ir išlaikomi prastai besimokantys",
                        "description": "Šiuo metu sunku vertinti ir rinktis studijų programas pagal jų kokybę, todėl aukštosios mokyklos vilioja studentus 'fasadiniais' pokyčiais.",
                        "supporting": False,
                    }
                ]
            }, {
                "id": 3,
                "group": "Socialinė politika",
                "name": "Šeimos koncepcija",
                "description": 'Ar sutinkate, kad šeima galėtų būti sudaroma tik santuokos pagrindu? (santuoka galima tik tarp vyro ir moters)',
                "arguments": [
                    {
                        "id": 6,
                        "name": "Naudinga ekonomiškai",
                        "description": "Tikslingu valstybės finansavimu skatinamos darbo rinkoje paklausios studijų kryptys ir mažinamas perteklinių studijų krypčių patrauklumas.",
                        "supporting": True,
                    }, {
                        "id": 7,
                        "name": "Priimami ir išlaikomi prastai besimokantys",
                        "description": "Šiuo metu sunku vertinti ir rinktis studijų programas pagal jų kokybę, todėl aukštosios mokyklos vilioja studentus 'fasadiniais' pokyčiais.",
                        "supporting": False,
                    }, {
                        "id": 8,
                        "name": "Teršia aplinką",
                        "description": "Šiuo metu sunku vertinti ir rinktis studijų programas pagal jų kokybę, todėl aukštosios mokyklos vilioja studentus 'fasadiniais' pokyčiais.",
                        "supporting": False,
                    }, {
                        "id": 9,
                        "name": "Trūksta informacijos",
                        "description": "Studijų programas pagal jų kokybę, todėl aukštosios mokyklos vilioja studentus 'fasadiniais' pokyčiais.",
                        "supporting": False,
                    }
                ]
            }
        ]

    def get(self, request):
        context = {
            'topics': self.topics_all(),
            'title': 'Seimo rinkimai 2016',
        }
        return render(request, self.template_name, context)


def topics_json(request):
    topics = topics_all()
    return JsonResponse({'items': topics})


class ResultsView(View):
    template_name = 'results.jade'

    def get(self, request):
        context = {
            'title': 'Seimo rinkimai 2016',
        }
        return render(request, self.template_name, context)
