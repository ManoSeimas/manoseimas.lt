from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import sboard.factory

sboard.factory.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'sboard.views.node', {'action': 'list'}, name='index'),
    url(r'^$', 'sboard.views.node', {'slug': 'testas'}, name='index'),
    url(r'^accounts/', include('social_auth.urls')),
    url(r'^accounts/', include('sboard.profiles.urls')),
    url(r'^paieska/', include('manoseimas.search.urls')),
    url(r'^istatymai/', include('manoseimas.legislation.urls')),
    url(r'', include('sboard.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
