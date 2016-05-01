from django.conf.urls import include, patterns, url

from manoseimas.compatibility_test import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='start_test'),
    url(r'question/?$',
        views.first_question, name='first_question'),
    url(r'question/(?P<question_slug>[-_\w]+)/$',
        views.question, name='question'),
)
