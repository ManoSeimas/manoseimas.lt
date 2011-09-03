from django.conf.urls.defaults import *

urlpatterns = patterns('legislation.views',
    url(r'^$', 'index', name='manoseimas-legislation-index'),
    url(r'^search/$', 'search', name='manoseimas-legislation-search'),
    url(r'^edit/(?P<doc_id>[a-z0-9-]+)/$', 'edit', name='manoseimas-legislation-edit'),
)
