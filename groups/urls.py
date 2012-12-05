from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("groups.views",
    url(r'^group/(?P<grpid>\d+)/$', 'group'),
    url(r'^create/$', 'create'),
    url(r'^group/(?P<grpid>\d+)/send_invites/$', 'send_invites'),
    url(r'^membership/(?P<memid>\d+)/remove/$', 'remove_member'),
)
