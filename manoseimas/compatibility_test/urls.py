from django.conf.urls import include, patterns, url

from manoseimas.compatibility_test import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index_view, name='start_test'),
)
