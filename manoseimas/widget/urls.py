from django.conf.urls.defaults import patterns, url

slug = r'[a-z0-9~+-]+'

urlpatterns = patterns('widget.views',
    url(r'^$', 'index'),
    url(r'^builder$', 'builder'),
    url(r'^data/voting/(?P<slug>%s)$' % slug, 'voting_data'),
    url('^auth/google/popup$', 'google_openid_mode_hack'),
    url('^auth/finish$', 'auth_finish'),
)
