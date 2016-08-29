# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import json

from django.shortcuts import redirect, render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
from django.http import JsonResponse
from django.conf import settings

from lazysignup.decorators import allow_lazy_user

from manoseimas.mps_v2.models import Group, ParliamentMember
from manoseimas.compatibility_test.models import CompatTest
from manoseimas.compatibility_test.models import Topic
from manoseimas.compatibility_test.models import UserResult


def topics_all(test_id):
    qs = Topic.objects.all()
    qs = qs.filter(groups__test_id=test_id)
    qs = qs.prefetch_related('groups', 'arguments')

    topics = []
    for topic in qs:
        arguments = topic.arguments.all().values(
            'id', 'name', 'short_description', 'description', 'supporting'
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
            'slug': topic.slug,
            'group': topic.groups.first().name,
            'description': topic.description,
            'arguments': list(arguments),
            'votings': votings,
            'image': topic.image.url if topic.image else None,
        })
    # TODO: randomise by group #153
    return topics


def get_current_test():
    return CompatTest.objects.order_by('id').first()


def get_test_by_id(test_id):
    if not test_id:
        return get_current_test()
    return CompatTest.objects.filter(id=test_id).first()


def get_test_context(test_id):
    test = get_test_by_id(test_id)
    topics = topics_all(test_id)
    return {
        'topics': topics,
        'first_topic': {
            'position': 0,
            'slug': topics[0]['slug'],
        },
        'title': test.name,
        'test_id': test.id,
        'test_img': test.image.url if test.image else None,
    }


@ensure_csrf_cookie
def start_test(request, test_id=None):
    if not test_id:
        test_id = get_current_test().id
        return redirect('start_test', test_id=test_id)

    return render(request, 'start_test.jade', get_test_context(test_id))


def topics_json(request, test_id=None):
    topics = topics_all(test_id)
    return JsonResponse({'items': topics})


class ResultsView(View):
    template_name = 'results.jade'

    def get_answers(self, user, test_id):
        if not user:
            return None

        test = get_test_by_id(test_id)
        results = UserResult.objects.filter(user_id=user.id, test=test).first()
        if results:
            return results.result
        else:
            return None

    def results(self, user=None, test_id=None):
        # Generate results by given test_id and user.
        # More requirements:
        # https://github.com/ManoSeimas/manoseimas.lt/issues/154

        term_of_office = '{0:%Y}-{1:%Y}'.format(*settings.TERM_OF_OFFICE_RANGE)
        return {
            'user_answers': self.get_answers(user, test_id),
            'fractions': [
                {
                    'id': group.pk,
                    'title': group.name,
                    'short_title': group.abbr,
                    'logo': group.logo.url if group.logo else None,
                    'answers': group.positions,
                    'members_amount': group.active_member_count,
                } for group in Group.objects.filter(type=Group.TYPE_FRACTION).order_by('pk')
            ],
            'mps': [
                {
                    'id': mp.pk,
                    'name': mp.full_name,
                    'fraction': mp.fraction.abbr if mp.fraction else None,
                    'fraction_id': mp.fraction.pk if mp.fraction else None,
                    'logo': mp.photo.url if mp.photo else None,
                    'answers': mp.positions,
                } for mp in ParliamentMember.objects.filter(term_of_office=term_of_office).order_by('pk')
            ]
        }

    def post(self, request, **kwargs):
        user = request.user
        test_id = kwargs.get('test_id', None)
        return JsonResponse(self.results(user, test_id))

    def get(self, request, **kwargs):
        user = request.user
        test_id = kwargs.get('test_id', None)
        context = {
            'title': 'Seimo rinkimai 2016',
            'test_id': test_id,
            'results': self.results(user),
        }
        return render(request, self.template_name, context)

test_results = ResultsView.as_view()


@allow_lazy_user
def answers_json(request, test_id=None):
    user = request.user
    test = get_test_by_id(test_id)
    answers = {}
    ur = UserResult.objects.filter(user=user, test=test).first()
    if request.method == 'POST':
        if not ur:
            ur = UserResult()
            ur.user = user
            ur.test = test
        answers = json.loads(request.body)
        ur.result = answers
        ur.save()
    else:
        answers = ur.result if ur else {}
    return JsonResponse({'answers': answers, 'test_id': test.id})
