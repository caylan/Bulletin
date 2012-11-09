'''
These models are for interuser communication.  These include, but are
not limited to: posting to groups, inviting other users to a group,
and commenting on posts in a group.
'''
from django.db import models
from django.contrib.auth.models import User
from groups.models import Group, Membership

# TODO
# class SeenBy(models.Model):
#     pass

class AbstractPost(models.Model):
    '''
    This is the base class for Post and Comment (they are rather similar),
    the only big difference being that a comment is related to a particular
    post.
    '''
    #author = models.ForeignKey(User)
    author = models.ForeignKey('groups.Membership')
    date_posted = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    class Meta:
        abstract = True
        ordering = ['-date_posted']  # newest first

    def __unicode__(self):
        return "{0} ({1})".format(self.author, \
                                  self.date_posted)

class Post(AbstractPost):
    ''' 
    Remove this once user login works! For now all users will have access
    to the (as of late) two static groups.  These groups will be here
    in order to ease up code mangling by trying to get both login
    and user->group posting working simultaneously.
    '''
    # group = models.ForeignKey(Group)
    pass

class Comment(AbstractPost):
    post = models.ForeignKey('Post')
    class Meta:
        ordering = ['date_posted']  # oldest first

