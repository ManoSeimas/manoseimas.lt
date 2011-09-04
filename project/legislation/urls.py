from django.conf.urls.defaults import *

urlpatterns = patterns('legislation.views',
    url(r'^$', 'document_list', name='manoseimas-legislation-document-list'),
    url(r'^paieska/$', 'document_search', name='manoseimas-legislation-document-search'),
    url(r'^istatymas/(?P<legislation_id>[a-z0-9-]+)/$', 'legislation', name='manoseimas-legislation-legislation'),
)
