from django.conf.urls.defaults import patterns, url

from manoseimas.mps_v2 import views


urlpatterns = patterns('',
    url('^$', views.mp_list),  # noqa
    url('^/?P<mp-slug>/', views.mp_profile),
)
