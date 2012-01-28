from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^accounts/', include('manoseimas.accounts.urls')),
    url(r'^accounts/', include('social_auth.urls')),
    url(r'^paieska/', include('manoseimas.search.urls')),
    url(r'^istatymai/', include('manoseimas.legislation.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
