from django.conf.urls import include, patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'manoseimas.lobbyists.views.lobbyists.lobbyist_list'),
    url(r'^json/', include('manoseimas.lobbyists.json_urls')),
)
