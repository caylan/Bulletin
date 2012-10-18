from prototype.models import Post, Comment
from django.contrib import admin

# Posts
class CommentInline(admin.TabularInline):
    model = Comment

class PostAdmin(admin.ModelAdmin):
    fields = ['group', 'author', 'message',]
    inlines = [CommentInline]

admin.site.register(Post, PostAdmin)




# Comments
class CommentAdmin(PostAdmin):
    fields = ['author', 'message','post',]

admin.site.register(Comment, CommentAdmin)

