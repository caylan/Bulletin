from django.db import models

"""
User stuffz
"""

class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=32)  # md5 hashed password
    salt = models.CharField(max_length=8)  # idk

class Session(models.Model):
    user = models.ForeignKey('User')
    token = models.CharField(max_length=32)

class Group(models.Model):
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Member(models.Model):
    user = models.ForeignKey('User')
    group = models.ForeignKey('Group')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField()

# class SeenBy(models.Model):
#     pass

class Invite(models.Model):
    is_active = models.BooleanField(default=True)
    recipient_email = models.EmailField()
    key = models.CharField(max_length=32)
    sent_by = models.ForeignKey('Member')
    expires = models.DateTimeField(null=True)  # null implies never expires

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

class Post(AbstractPost):
    pass

class Comment(AbstractPost):
    post = models.ForeignKey(Post)
    class Meta:
        ordering = ['date_posted']  # oldest first

