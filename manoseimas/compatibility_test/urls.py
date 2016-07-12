from django.conf.urls import include, patterns, url

from manoseimas.compatibility_test import views


test_urls = patterns(
    '',
    url(r'^$', views.start_test, name='start_test'),
    url(r'^topics/?$', views.topics_json, name='topics_json'),
    url(r'^answers/?$', views.answers_json, name='answers_json'),
    url(r'^results/?$', views.test_results, name='test_results'),
    url(r'^shared/(?P<results_hash>[-_\w]+)/$',
        views.shared_test, name='shared_test'),
)

urlpatterns = patterns(
    '',
    url(r'^$', views.start_test),
    url(r'^(?P<test_id>\d+)/', include(test_urls)),
)
