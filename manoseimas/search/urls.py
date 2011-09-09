from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('manoseimas.search.views',
    url(r'^$', 'search_results', name='manoseimas-search-results'),
)

