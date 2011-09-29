from django.conf.urls.defaults import *

LEGISLATION_ID = r'(?P<legislation_id>[A-Za-z0-9\(\)-]+)'

urlpatterns = patterns('manoseimas.legislation.views',
    url(r'^$', 'legislation_list', name='manoseimas-legislation-list'),
    url(r'^paieska/$', 'document_search',
        name='manoseimas-legislation-document-search'),
    url(r'^%s/$' % LEGISLATION_ID, 'legislation',
        name='manoseimas-legislation'),
    url(r'^%s/pataisos/$' % LEGISLATION_ID, 'legislation_amendments',
        name='manoseimas-legislation-amendments'),
    url(r'^%s/projektai/$' % LEGISLATION_ID, 'legislation_drafts',
        name='manoseimas-legislation-drafts'),
    url(r'^projektai/$', 'legislation_all_drafts',
        name='manoseimas-legislation-all-drafts'),
)
