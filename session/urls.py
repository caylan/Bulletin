from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns("session.views",
    url(r'^logout/$', 'logout_view'),
    url(r'^$', 'login_view'),
)

