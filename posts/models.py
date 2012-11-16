'''
These models are for interuser communication.  These include, but are
not limited to: posting to groups, inviting other users to a group,
and commenting on posts in a group.
'''
from django.db import models
from django.contrib.auth.models import User
from django.template import Template, Context  # for rendering to JSON string.
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

    def time_stamp(self):
        return self.date_posted.isoformat()

    def json(self):
        '''
        generate JSON for the post/comment object, intended to be returned via AJAX
        '''
    
        # Use the implicit template formatting rather than the __str__
        # formatting, which is default if we were to return a formatted string.
        json_template = Template('''
            {
                "author":
                {
                    "email": "{{ email }}",
                    "first_name": "{{ first_name }}",
                    "last_name": "{{ last_name }}"
                },
                "date_posted": "{{ date_posted }}",
                "time_stamp": "{{ time_stamp }}",
                "message": "{{ message }}"
            }''')
        ctx = Context({
                'email': self.author.user.email,
                'first_name': self.author.user.first_name,
                'last_name': self.author.user.last_name,
                'date_posted': self.date_posted,
                'time_stamp': self.time_stamp(),
                'message': self.message,
        })
        return json_template.render(ctx)

class Post(AbstractPost):
    pass

class Comment(AbstractPost):
    post = models.ForeignKey('Post')
    class Meta:
        ordering = ['date_posted']  # oldest first

