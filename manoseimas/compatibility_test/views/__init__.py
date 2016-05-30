# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = 'start_test.jade'

    def topics(self):
        return [
            {
                "name": "Aukštojo mokslo reforma",
                "description": 'Ar pritariate aukštojo mokslo reformai, įvedusiai "krepšelių" finansavimą, pakeitusiai aukštųjų mokyklų valdymą ir kt.?',
            }, {
                "name": "Šeimos koncepcija",
                "description": 'Ar sutinkate, kad šeima galėtų būti sudaroma tik santuokos pagrindu? (santuoka galima tik tarp vyro ir moters)'
            }, {
                "name": 'Visagino atominė elektrinė',
                "description": 'Ar pritariate Visagino atominės elektrinės statybai Lietuvoje?'
            }
        ]

    def get(self, request):
        return render(request, self.template_name, {'topics': self.topics})


def question(request, question_slug):
    return render(request, 'test_question.jade', {'question': question_slug})


def first_question(request):
    return question(request, 'first')
