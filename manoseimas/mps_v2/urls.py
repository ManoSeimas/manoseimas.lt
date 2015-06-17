from django.conf.urls import patterns, url

from manoseimas.mps_v2 import views


urlpatterns = patterns(
    '',
    url(r'^$', views.mp_list, name='mp_list_all'),
    url(r'^test_jsx$', views.jsx_test_view),
    url(r'^fractions/?$',
        views.mp_fraction_list, name='mp_fraction_list'),
    url(r'^discussion/(?P<statement_id>\d+)$',
        views.mp_discussion, name='mp_discussion'),
    url(r'^discussion_json/(?P<statement_id>\d+)$',
        views.mp_discussion_json, name='mp_discussion_json'),
    url(r'^fractions/(?P<fraction_slug>[-_\w]+)/$',
        views.mp_fraction, name='mp_fraction'),
    url(r'^parliamentarian/(?P<mp_slug>.+)/$',
        views.mp_profile, name='mp_profile'),
    url(r'^statements/(?P<mp_slug>[-_\w]+)/(?P<statement_page>.+)/$',
        views.mp_statements, name='mp_statements_paged'),
    url(r'^statements/(?P<mp_slug>.+)/$',
        views.mp_statements, name='mp_statements'),
    url(r'^(?P<fraction_slug>[-_\w]+)/$',
        views.mp_list, name='mp_list_fraction'),
)
