'''
These models are for interuser communication.  These include, but are
not limited to: posting to groups, inviting other users to a group,
and commenting on posts in a group.
'''
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# TODO
# class SeenBy(models.Model):
#     pass

class AbstractPost(models.Model):
    '''
    This is the base class for Post and Comment (they are rather similar),
    the only big difference being that a comment is related to a particular
    post.
    '''
    author = models.ForeignKey(User)
    # TODO(kyle) temp, have author point to a user until Membership stuff is implemented
    # author = models.ForeignKey('groups.Membership')
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
    # TODO(kyle) remove this when groups/membership is implemented
    group = models.PositiveIntegerField()
    pass

class PostForm(ModelForm):
    """
    Form for the post model
    """
    class Meta:
        model = Post
        # the following should be set by the view depending on context
        exclude = ['author', 'group',]

class Comment(AbstractPost):
    post = models.ForeignKey('Post')
    class Meta:
        ordering = ['date_posted']  # oldest first

