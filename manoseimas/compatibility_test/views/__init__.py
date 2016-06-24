# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.http import JsonResponse

from lazysignup.decorators import allow_lazy_user

from manoseimas.compatibility_test.models import CompatTest
from manoseimas.compatibility_test.models import Topic
from manoseimas.compatibility_test.models import UserResult


def topics_all(test_id=None):
    qs = Topic.objects.all()
    if not test_id:
        test_id = get_current_test().id
    qs = qs.filter(groups__test_id=test_id)
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


def get_current_test():
    return CompatTest.objects.order_by('id').first()


@ensure_csrf_cookie
def start_test(request, test_id=None):
    if not test_id:
        test_id = get_current_test().id
    test = CompatTest.objects.get(id=test_id)
    context = {
        'topics': topics_all(test_id),
        'title': test.name,
    }
    return render(request, 'start_test.jade', context)


def topics_json(request, test_id=None):
    topics = topics_all(test_id)
    return JsonResponse({'items': topics})


class ResultsView(View):
    template_name = 'results.jade'

    def results(self, test_id=None, user_id=None):
        # Generate results by given test_id and user_id.
        # More requirements:
        # https://github.com/ManoSeimas/manoseimas.lt/issues/154

        if not test_id:
            test_id = get_current_test().id

        return {
            'user_answers': {},
            'fractions': [
                {
                    'title': 'Darbo partijos frakcija',
                    'short_title': 'DP',
                    'logo': '/media/fraction_logos/dp.jpg',
                    'answers': {'1': 1, '2': 0.3, '3': 0.5, '4': -0.8, '5': 0},
                    'members_amount': 21,
                }, {
                    'title': 'Liberalų sąjūdžio frakcija',
                    'short_title': 'LLS',
                    'logo': '/media/fraction_logos/lls.jpg',
                    'answers': {'1': 0.5, '2': -0.3, '3': 0.5, '4': -0.8, '5': 1},
                    'members_amount': 10,
                }, {
                    'title': 'Lietuvos lenkų rinkimų akcijos frakcija',
                    'short_title': 'LLRA',
                    'logo': '/media/fraction_logos/llra.jpg',
                    'answers': {'1': 0.75, '2': 1, '3': -0.8, '4': -1, '5': 0},
                    'members_amount': 4,
                }
            ],
            'mps': [
                {
                    'id': 1,
                    'name': 'Jonas Jonaitis',
                    'fraction': 'DP',
                    'logo': '/media/profile_images/00a6a60429383aaa36a868c2595a06c88e6422b0.jpg',
                    'answers': {'1': 1, '2': -0.3, '3': 0.5, '4': -0.8, '5': 0}
                }, {
                    'id': 2,
                    'name': 'Petras Petraitis',
                    'fraction': 'LLRA',
                    'logo': '/media/profile_images/01667d36a4df869561133dfe44a39ca881ce2b5e_PpSk71U.jpg',
                    'answers': {'1': 1, '2': 0.5, '3': 1, '4': -0.8, '5': 0}
                }, {
                    'id': 3,
                    'name': 'Jonas Petraitis',
                    'fraction': 'LLRA',
                    'logo': '/media/profile_images/01ffb49169abd4606343aa2e9e621e527fa1013e_yDdIUBb.jpg',
                    'answers': {'1': -0.8, '2': 1, '3': 0.5, '4': -1, '5': 1}
                }, {
                    'id': 4,
                    'name': 'Petras Jonaitis',
                    'fraction': 'LLS',
                    'logo': '/media/profile_images/0c5b864efce2278579c4a1a0fa1985851454c244_TViMIZR.jpg',
                    'answers': {'1': 0.5, '2': -1, '3': 0.5, '4': -0.8, '5': -1}
                }
            ]
        }

    def post(self, request):
        return JsonResponse(self.results())

    def get(self, request):
        context = {
            'title': 'Seimo rinkimai 2016',
            'results': self.results()
        }
        return render(request, self.template_name, context)


@allow_lazy_user
def answers_json(request):
    user = request.user
    answers = {}
    results = UserResult.objects.filter(user=user)
    if request.method == 'POST':
        if results:
            ur = results[0]
        else:
            ur = UserResult()
            ur.user = user
        answers = json.loads(request.body)
        ur.result = answers
        ur.save()
    else:
        if results:
            ur = results[0]
            answers = ur.result
    return JsonResponse({'answers': answers, 'user': user.id})
