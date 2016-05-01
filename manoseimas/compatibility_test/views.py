from django.shortcuts import render


def index(request):
    return render(request, 'start_test.jade', {})


def question(request, question_slug):
    return render(request, 'test_question.jade', {'question': question_slug})


def first_question(request):
    return question(request, 'first')

