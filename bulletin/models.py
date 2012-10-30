from django.db import models

"""
User stuffz
"""

class User(models.Model):
    '''
    A user is the main abstraction of a user account on the
    website.
    '''
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=32)  # md5 hashed password
    salt = models.CharField(max_length=8)  # idk

    def __unicode__(self):
        return "{0}, {1}: {2}".format(self.first_name, self.last_name, self.email)

class Session(models.Model):
    user = models.ForeignKey('User')
    token = models.CharField(max_length=32)

    def __unicode__(self):
        return "{0} ({2})".format(self.user.first_name, self.token)

class Group(models.Model):
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "{0} -- {1} (Active={2})".format(self.name.__unicode__(), \
                                                self.date_created.__unicode__(), \
                                                self.is_active.__unicode__())

class Member(models.Model):
    '''
    This ties a user to a group via a membership.
    '''
    user = models.ForeignKey('User')
    group = models.ForeignKey('Group')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField()

    def __unicode__(self):
        return "{0}: {1} ({2})".format(self.user.first_name, \
                                       self.group.name, \
                                       self.date_joined.__unicode__())

# class SeenBy(models.Model):
#     pass

class Invite(models.Model):
    is_active = models.BooleanField(default=True)
    recipient_email = models.EmailField()
    key = models.CharField(max_length=32)
    sent_by = models.ForeignKey('Member')
    expires = models.DateTimeField(null=True)  # null implies never expires

    def __unicode__(self):
        return "{0}: {1} (Active={2})".format(self.recipient_email.__unicode__(), \
                                              self.expires.__unicode__(). \
                                              self.is_active)

"""
Post stuffz
"""

class AbstractPost(models.Model):
    author = models.ForeignKey('Member')
    date_posted = DateTimeField(auto_now_add=True)
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

