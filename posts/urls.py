from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("posts.views",
    url(r'^post/(?P<postid>\d+)/comment/$', 'comment'),
)