from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# if $DEVELOPMENT
from django.contrib import admin


admin.autodiscover()
# end if

import sboard.factory

sboard.factory.autodiscover()

import manoseimas.docutils_roles

import manoseimas.set_session_expiry  # noqa


urlpatterns = patterns('',
    url(r'^$', 'views.index'),  # noqa
    url(r'^search.json$', 'views.ajax_search'),
    url(r'^accounts/', include('social_auth.urls')),
    url(r'^accounts/', include('sboard.profiles.urls')),

    url(r'^widget/', include('widget.urls')),
    url(r'^mp/', include('mps_v2.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {  # noqa
                'document_root': settings.MEDIA_ROOT,
            }),
       )
    # if $DEVELOPMENT
    urlpatterns += patterns('', (r'^admin/', include(admin.site.urls)))
    # end if

urlpatterns += patterns('', url(r'', include('sboard.urls')))
