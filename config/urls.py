from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import sboard.factory

sboard.factory.autodiscover()

import manoseimas.docutils_roles

import manoseimas.set_session_expiry

urlpatterns = patterns('',
    url(r'^$', 'sboard.views.node_view', {'slug': 'manoseimas'}, name='index'),
    url(r'^accounts/', include('social_auth.urls')),
    url(r'^accounts/', include('sboard.profiles.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                'document_root': settings.MEDIA_ROOT,
            }),
       )

urlpatterns += patterns('', url(r'', include('sboard.urls')))
