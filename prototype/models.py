from django.db import models

class UserPost(models.Model):
    author = models.EmailField()
    message = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.time_posted.isoformat() + " | " + self.author + " | " + self.message[:20]
    
    class Meta:
        abstract = True
        ordering = ['-time_posted']

class Post(UserPost):
    pass

class Comment(UserPost):
    post = models.ForeignKey(Post)
