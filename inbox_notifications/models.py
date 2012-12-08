from django.db import models
from django.contrib.auth.models import User
from posts.models import Post, Comment

class __AbstractNotification(models.Model):
    '''
    Refers to any sort of notification.  A notification can have been read, and
    has a date that it was created.
    '''
    has_been_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        abstract = True

class PostNotification(__AbstractNotification):
    '''
    A notification for a post.  Points to the post related to the notification,
    and has several utilities for getting the url of the post, the message
    representation of the post, etc.
    '''

    type_ = "post"  # for use in templates only.
    content = models.ForeignKey(Post)

    def get_uri(self):
        '''
        Gets the uri for the post.

        NOTE: This depends on the views for groups.  If the URI changes there,
        sadly it must change here.
        '''
        grpid = post.author.group.pk
        return u'group/{0}/#post{0}'.format(grpid, self.post.pk)

class CommentNotification(__AbstractNotification):
    '''
    A notification for a comment.  Points to the comment related to the post.
    '''

    type_ = "comment"  # for use in templates only.
    content = models.ForeignKey(Comment)

    def get_uri(self):
        '''
        Gets the uri for the comment.

        NOTE: This depends on the views for the groups, similar to the post
        notification, and if this changes, then so must the notification for the
        post.
        '''
        grpid = comment.author.group.pk
        return u'group/{0}/#comment{0}/'.format(grpid, self.comment.pk)
