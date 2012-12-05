from django.conf.urls.defaults import patterns, include, url

# NOTE: If any of this changes, the uri generator in inbox.models will need to
# change, as it generates links to these view methods, and we don't want to run
# into 404 error messages.
#
# The current solution to this problem would be to use something similar to
# Java's xeger to generatr a string from a regex, given the ids are the same,
# but the current implementations of xeger for python doesn't allow setting the ID
# params within the regex, which is the only reason we'd want to use it.


urlpatterns = patterns("groups.views",
    url(r'^group/(?P<grpid>\d+)/$', 'group'),
    url(r'^create/$', 'create'),
    url(r'^group/(?P<grpid>\d+)/send_invites/$', 'send_invites')
)
