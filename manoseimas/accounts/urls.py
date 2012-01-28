from django.conf.urls.defaults import patterns, url

from manoseimas.utils import reverse_lazy


urlpatterns = patterns('manoseimas.accounts.views',
    url(r'^profile/$', 'profile', name='ms_profile'),
    url(r'^login/$', 'login', name='ms_login'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^logout/', 'logout', {'next_page': reverse_lazy('index')},
        name="ms_logout"),
)
