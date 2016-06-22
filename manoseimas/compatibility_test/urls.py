from django.conf.urls import include, patterns, url

from manoseimas.compatibility_test.views import start_test
from manoseimas.compatibility_test.views import ResultsView

urlpatterns = patterns(
    '',
    url(r'^$', start_test, name='start_test'),
    url(r'results/(?P<user_id>[-_\w]+)/$',
        ResultsView.as_view(), name='test_results'),
    url(r'^json/', include('manoseimas.compatibility_test.json_urls')),
)
