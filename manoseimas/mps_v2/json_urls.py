from django.conf.urls import patterns, url

from manoseimas.mps_v2 import views


urlpatterns = patterns(
    '',
    url(r'^fractions/?$', views.fractions_json, name='fractions_json'),
    url(r'^mps/?$', views.mps_json, name='mps_json'),
    url(r'^law_projects/(?P<mp_slug>.+)/?$',
        views.law_projects_json, name='law_projects_json'),
    url(r'^discussion/(?P<statement_id>\d+)/?$',
        views.mp_discussion_json, name='mp_discussion_json'),
)
