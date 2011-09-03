from django.conf.urls.defaults import *

urlpatterns = patterns('legislation.views',
    url(r'^$', 'index', name='manoseimas-legislation-index'),
)
