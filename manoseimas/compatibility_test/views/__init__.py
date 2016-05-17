from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = 'start_test.jade'

    def get(self, request):
        return render(request, self.template_name, {})


def question(request, question_slug):
    return render(request, 'test_question.jade', {'question': question_slug})


def first_question(request):
    return question(request, 'first')
