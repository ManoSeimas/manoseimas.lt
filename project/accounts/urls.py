from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^profile/$', 'legislation.views.document_list'),
)

