from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'manoseimas.lobbyists.views.lobbyists.lobbyist_list'),
)
