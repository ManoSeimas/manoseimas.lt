from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
    (r'^accounts/', include('manoseimas.accounts.urls')),
    (r'^paieska/', include('manoseimas.search.urls')),
    (r'^istatymai/', include('manoseimas.legislation.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
