from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'sboard.views.node', {'view': 'list'}, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('manoseimas.accounts.urls')),
    url(r'^accounts/', include('social_auth.urls')),
    url(r'^paieska/', include('manoseimas.search.urls')),
    url(r'^accounts/', include('sboard.profiles.urls')),
    url(r'^istatymai/', include('manoseimas.legislation.urls')),
    url(r'', include('sboard.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
