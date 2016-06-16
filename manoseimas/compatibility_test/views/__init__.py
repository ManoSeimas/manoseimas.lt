# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View


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
            'topics': self.topics,
            'title': 'Seimo rinkimai 2016',
        }
        return render(request, self.template_name, context)


class ResultsView(View):
    template_name = 'results.jade'

    def get(self, request):
        context = {
            'title': 'Seimo rinkimai 2016',
        }
        return render(reques, self.template_name, context)
