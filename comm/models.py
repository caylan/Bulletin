'''
These models are for interuser communication.  These include, but are
not limited to: posting to groups, inviting other users to a group,
and commenting on posts in a group.
'''
from django.db import models
from django.contrib.auth.models import User

# class SeenBy(models.Model):
#     pass

class Invite(models.Model):
    '''
    An invite is something sent from one user to another in order
    to get people to join the website (or, if they're already a member
    of the website, to get them to join the group)
    '''
    is_active = models.BooleanField(default=True)
    recipient_email = models.EmailField()
    key = models.CharField(max_length=32)
    sent_by = models.ForeignKey(User) 
    expires = models.DateTimeField(null=True)  # null implies never expires

    def __unicode__(self):
        return "{0}: {1} (Active={2})".format(self.recipient_email.__unicode__(), \
                                              self.expires.__unicode__(). \
                                              self.is_active)
"""
Post stuffz
"""

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
        return "{0} ({1})".format(self.author.__unicode__(), \
                                  self.date_posted.__unicode__())

class Post(AbstractPost):
    pass

class Comment(AbstractPost):
    post = models.ForeignKey(Post)
    class Meta:
        ordering = ['date_posted']  # oldest first

