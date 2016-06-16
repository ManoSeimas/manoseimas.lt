from django.conf.urls import patterns, url

from manoseimas.compatibility_test.views import IndexView
from manoseimas.compatibility_test.views import ResultsView

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='start_test'),
    url(r'results/(?P<user_id>[-_\w]+)/$',
        ResultsView.as_view(), name='test_results'),
)
