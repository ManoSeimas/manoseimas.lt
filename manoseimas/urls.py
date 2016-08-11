from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

import manoseimas.set_session_expiry  # noqa

from manoseimas.flatpages.views import flatpage_view


admin.autodiscover()

flatpage_patterns = [
    url(r'^about/(?P<page>[-_\w]+)/$', flatpage_view, name='flatpage'),
    url(r'^about/?$', flatpage_view, kwargs={'page': 'about'}, name='about'),
]

urlpatterns = patterns(
    '',
    url(r'^$', 'manoseimas.views.index'),
    url(r'^influence/?$', 'manoseimas.views.influence', name='influence'),
    url(r'^votings/?$', 'manoseimas.views.votings'),
    url(r'^search/',
        include('haystack.urls')),
    url(r'^accounts/',
        include('social.apps.django_app.urls', namespace='social')),
    url(r'^login/',
        'manoseimas.views.login', name="login"),
    url(r'^logout/',
        'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),

    url(r'^widget/', include('manoseimas.widget.urls')),
    url(r'^mp/', include('manoseimas.mps_v2.urls')),
    url(r'^json/', include('manoseimas.mps_v2.json_urls')),
    url(r'^lobbyists/', include('manoseimas.lobbyists.urls')),
    url(r'^test/', include('manoseimas.compatibility_test.urls')),
    url('^', include(flatpage_patterns)),
    url(r'^valdymas/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
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
