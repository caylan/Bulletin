from django.contrib import admin
from bulletin import models

# Posts
class CommentInline(admin.TabularInline):
    model = models.Comment

class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'date_posted', 'message',)
    readonly_fields = ('date_posted',)
    inlines = (CommentInline,)

admin.site.register(models.Post, PostAdmin)

###
