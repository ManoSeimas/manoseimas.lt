from django.conf.urls import patterns, url

from manoseimas.mps_v2 import views


urlpatterns = patterns('',
    url(r'^$', views.mp_list, name='mp_list_all'),
    url(r'^fractions/?$', views.mp_fraction_list, name='mp_fraction_list'),
    url(r'^fractions/(?P<fraction_slug>[-_\w]+)/$', views.mp_fraction, name='mp_fraction'),
    url(r'^parliamentarian/(?P<mp_slug>.+)/$', views.mp_profile, name='mp_profile'),
    url(r'^(?P<fraction_slug>[-_\w]+)/$', views.mp_list, name='mp_list_fraction'),
)
