from django.conf import settings
from django.shortcuts import render


def profile(request):
    template = 'manoseimas/accounts/profile.html'
    return render(request, template)


def login(request):
    template = 'manoseimas/accounts/login.html'
    return render(request, template, {'settings': settings})
