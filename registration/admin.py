from django.contrib import admin

from registration.models import EmailConfirmation, EmailInvite

admin.site.register(EmailConfirmation)
admin.site.register(EmailInvite)
