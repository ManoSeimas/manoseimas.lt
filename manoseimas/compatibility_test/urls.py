from django.conf.urls import patterns, url

from manoseimas.compatibility_test.views import IndexView
from manoseimas.compatibility_test.views import question
from manoseimas.compatibility_test.views import first_question


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='start_test'),
    url(r'question/?$',
        first_question, name='first_question'),
    url(r'question/(?P<question_slug>[-_\w]+)/$',
        question, name='question'),
)
