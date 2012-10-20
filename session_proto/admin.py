from session_proto.models import User, Session
from django.contrib import admin

# User
class SessionInline(admin.TabularInline):
    model = Session
    extra = 0

class UserAdmin(admin.ModelAdmin):
    fields = (('first_name', 'last_name'), 'email', 'password', 'date_joined')
    readonly_fields = ('date_joined',)
    inlines = [SessionInline]

admin.site.register(User, UserAdmin)




# Session
class SessionAdmin(admin.ModelAdmin):
    fields = ('user', 'token', 'ip', 'time_created',)
    readonly_fields = ('user', 'token', 'ip', 'time_created',)

admin.site.register(Session, SessionAdmin)

