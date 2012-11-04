from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("groups.views",
        url(r'^group/(?P<grpid>\d+)/$', 'group'),
)
