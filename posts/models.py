'''
These models are for interuser communication.  These include, but are
not limited to: posting to groups, inviting other users to a group,
and commenting on posts in a group.
'''
from django.db import models
from django.contrib.auth.models import User

# class SeenBy(models.Model):
#     pass

class AbstractPost(models.Model):
    '''
    This is the base class for Post and Comment (they are rather similar),
    the only big difference being that a comment is related to a particular
    post.
    '''
    author = models.ForeignKey(User)
    date_posted = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    class Meta:
        abstract = True
        ordering = ['-date_posted']  # newest first

    def __unicode__(self):
        return "{0} ({1})".format(self.author, \
                                  self.date_posted)

class Post(AbstractPost):
    ''' Remove this once user login works! '''
    group = models.PositiveIntegerField()
    pass

class Comment(AbstractPost):
    post = models.ForeignKey(Post)
    class Meta:
        ordering = ['date_posted']  # oldest first

