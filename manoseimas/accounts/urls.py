from django.conf.urls.defaults import *


urlpatterns = patterns('manoseimas.legislation.views',
    url(r'^profile/$', 'legislation_list'),
)

