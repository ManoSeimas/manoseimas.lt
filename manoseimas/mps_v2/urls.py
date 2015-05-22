from django.conf.urls.defaults import patterns, url

from manoseimas.mps_v2 import views


urlpatterns = patterns('',
    url(r'^$', views.mp_list, name='mp_list'),  # noqa
    url(r'^(\d+)/', views.mp_profile, name='mp_profile'),
)
