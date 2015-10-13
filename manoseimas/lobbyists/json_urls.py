from django.conf.urls import patterns, url

from manoseimas.lobbyists import views

urlpatterns = patterns(
    '',
    url(r'^lobbyists/$', views.lobbyists_json, name='lobbyists_json'),
    url(r'^law_projects/(?P<lobbyist_slug>.+)/?$',
        views.law_projects_json, name='law_projects_json'),
)
