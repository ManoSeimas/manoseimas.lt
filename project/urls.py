from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from .views import *

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
    url(r'^accounts/profile', index, name='index'),
    url(r'^$', index, name='index'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
