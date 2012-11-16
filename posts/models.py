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
    author = models.ForeignKey('groups.Membership')
    date_posted = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    class Meta:
        abstract = True
        ordering = ['-date_posted']  # newest first

    def __unicode__(self):
        return "{0} ({1})".format(self.author, self.date_posted)

    def json(self):
        '''
        generate JSON for the post/comment object, intended to be returned via AJAX
        '''
        json_string = '''
            {{
                "author":
                {{
                    "email":"{0}",
                    "first_name": "{1}",
                    "last_name": "{2}"
                }},
                "date_posted": "{3}",
                "message": "{4}"
            }}'''
        return json_string.format(self.author.user.email,
                                  self.author.user.first_name,
                                  self.author.user.last_name,
                                  self.date_posted,
                                  self.message)

class Post(AbstractPost):
    pass

class Comment(AbstractPost):
    post = models.ForeignKey('Post')
    class Meta:
        ordering = ['date_posted']  # oldest first

