from django.contrib import admin
import models

# Group
"""
    GROUP
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField(User, through='Membership')
    
    MEMBERSHIP
    user = models.ForeignKey(User)
    group = models.ForeignKey('Group')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField()
"""
class MembershipInline(admin.TabularInline):
    model = models.Membership
    fields = ('user', 'date_joined', 'is_admin',)
    readonly_fields = ('date_joined',)

class GroupAdmin(admin.ModelAdmin):
    fields = ('name', 'date_created', 'is_active',)
    readonly_fields = ('date_created',)
    inlines = (MembershipInline,)

admin.site.register(models.Group, GroupAdmin)

