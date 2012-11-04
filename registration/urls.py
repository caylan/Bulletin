from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("registration.views",
    url(r'^confirm/(\w+)/$', 'confirm_email'),
    url(r'^register/$', 'register'),
)
