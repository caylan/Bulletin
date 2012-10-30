from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulletin_project.views.home', name='home'),
    # url(r'^bulletin_project/', include('bulletin_project.foo.urls')),
    url(r'^prototype/$', 'bulletin.views.index'),
    url(r'^prototype/group/(?P<grpid>\d+)/$', 'bulletin.views.group'),
    url(r'^prototype/login/$', 'session.views.login'),
    url(r'^prototype/register/$', 'session.views.register'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
