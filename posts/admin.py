from django.contrib import admin
import models

# Posts
class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0

class PostAdmin(admin.ModelAdmin):
    fields = ('author', 'date_posted', 'message', 'group')
    readonly_fields = ('date_posted',)
    inlines = (CommentInline,)

admin.site.register(models.Post, PostAdmin)

###
