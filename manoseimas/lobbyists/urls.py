from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'manoseimas.lobbyists.views.lobbyist_list.lobbyist_list'),
)
