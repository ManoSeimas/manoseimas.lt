from django.conf.urls import patterns, url

from manoseimas.compatibility_test import views


urlpatterns = patterns(
    '',
    url(r'^topics/?$', views.topics_json, name='topics_json'),
)
