from django.conf.urls import patterns, url

from manoseimas.mps_v2 import views


urlpatterns = patterns('',
    url(r'^$', views.mp_list, name='mp_list_all'),
    url(r'^(?P<fraction_slug>[-_\w]+)/$', views.mp_list, name='mp_list_fraction'),
    url(r'^parliamentarian/(\d+)/', views.mp_profile, name='mp_profile'),
)
