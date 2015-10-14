from django.conf.urls import include, patterns, url

from manoseimas.lobbyists import views

urlpatterns = patterns(
    '',
    url(r'^$', 'manoseimas.lobbyists.views.lobbyists.lobbyist_list'),
    url(r'^lobbyist/(?P<lobbyist_slug>.+)/?$',
        views.lobbyist_profile, name='lobbyist_profile'),
    url(r'^json/', include('manoseimas.lobbyists.json_urls')),
)
 
