from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulletin_project.views.home', name='home'),
    # url(r'^bulletin_project/', include('bulletin_project.foo.urls')),
    url(r'^$', 'session.views.login_view'),
    url(r'^group/(?P<grpid>\d+)/$', 'groups.views.group'),
    url(r'^register/$', 'registration.views.register'),
    url(r'^logout/$', 'session.views.logout_view'),
    url(r'^confirm_email/(\w+)/$', 'registration.views.confirm_email')
    
    # Post to group
    #url(r'^group/(?<grpid>\d+)/post/$', 'groups.views.post'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
