from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulletin_project.views.home', name='home'),
    # url(r'^bulletin_project/', include('bulletin_project.foo.urls')),
    url("", include("groups.urls")),
    url("", include("posts.urls")),
    url("", include('registration.urls')),
    url("", include('session.urls')),
    url("", include('inbox_notifications.urls')),
    url(r'^about/$', direct_to_template, {
        'template': 'about.html',
    }),
    
    # Post to group
    #url(r'^group/(?<grpid>\d+)/post/$', 'groups.views.post'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
