from django.http import HttpResponse

from .models import ParliamentMember


def mp_list(request):
    mps = ParliamentMember.objects.all()
    return HttpResponse('<br/>'.join(map(str, mps)))


def mp_profile(request):
    pass
