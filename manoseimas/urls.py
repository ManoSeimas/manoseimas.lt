from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

import sboard.factory

sboard.factory.autodiscover()

import manoseimas.docutils_roles
import manoseimas.set_session_expiry  # noqa

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'manoseimas.views.index'),  # noqa
    url(r'^search.json$', 'manoseimas.views.ajax_search'),
    url(r'^accounts/', include('social_auth.urls')),
    url(r'^accounts/', include('sboard.profiles.urls')),

    url(r'^widget/', include('manoseimas.widget.urls')),
    url(r'^mp/', include('manoseimas.mps_v2.urls')),
    url(r'^valdymas/', include(admin.site.urls)),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {  # noqa
                'document_root': settings.MEDIA_ROOT,
            }),
       )
    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)))

urlpatterns += patterns('', url(r'', include('sboard.urls')))
