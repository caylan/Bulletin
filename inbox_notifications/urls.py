from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("inbox_notifications.views",
    url(r'^/update/$', 'update'),
)
