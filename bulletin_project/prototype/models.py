from django.db import models

class Post(models.Model):
    author = models.EmailField()
    message = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.author + " | " + message[:20]

class Comment(models.Model):
    author = models.EmailField()
    message = models.TextField()
    post = models.ForeignKey('Post')
    time_posted = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.author + " | " + message[:20]

