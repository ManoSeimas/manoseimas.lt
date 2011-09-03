from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
    (r'^accounts/', include('accounts.urls')),
    (r'', include('legislation.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
