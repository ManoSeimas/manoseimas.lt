from django.conf.urls.defaults import *

urlpatterns = patterns('legislation.views',
    url(r'^$', 'index', name='manoseimas-legislation-index'),
    url(r'^search/$', 'search', name='manoseimas-legislation-search'),
    url(r'^legislation/(?P<legislation_id>[a-z0-9-]+)/$', 'legislation', name='manoseimas-legislation-legislation'),
)
