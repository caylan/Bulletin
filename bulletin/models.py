from django.db import models
from django.contrib.auth.models import (
    User
)

"""
This is where the basic user info is made.
"""

class BulletinUser(User):
    '''
    This is a custom class overriding the default class inherited
    from django.contrib.auth.models.User

    This simply adds in a few extra functions that'll be handy for 
    '''
    def is_in_group(self):
        return bool(self.groups.all())

    def is_group_admin(self, group):
        '''
        Determines if the user is the admin of a group.
        '''
        pass

class Group(models.Model):
    '''
    This is different from the groups in django's contrib.auth
    implementation, which are more like unix groups.  This keeps
    track of the groups a member is in on Bulletin.

    A bulletin user has a many to many relationship between this class
    and the membership class (the membership defines when and how the
    user became a member of this group)
    '''
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField(BulletinUser, through='Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    '''
    A membership determines the relation between a bulletin user and
    a group.  A user can or cannot be an admin of the group.

    There can also be multiple admins.
    '''
    user = models.ForeignKey(BulletinUser)
    group = models.ForeignKey(Group)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField()

    def __unicode__(self):
        return self.name
