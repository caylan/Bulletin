from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns("registration.views",
    url(r'^confirm/(\w+)/$', 'confirm_email'),
    url(r'^register/$', 'register'),
    url(r'^confirm_email_invite/(\w+)/$', 'confirm_email_invite'),
    url(r'^change_password/$', 'change_password'),
    url(r'^reset_password/$', 'reset_password'),
    url(r'^invite_registration/(\w+)/$', 'invite_registration'),
    url(r'^send_invites/$', 'send_invites'),
)
