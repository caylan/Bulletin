from django.db import models
from django.contrib.auth.models import (
    User
)

"""
This is where the basic user info is made.
"""
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

    ''' So it's called 'members' instead of user_set (implicitly) '''
    members = models.ManyToManyField(User, through='Membership')

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    '''
    A membership determines the relation between a bulletin user and
    a group.  A user can or cannot be an admin of the group.

    There can also be multiple admins.
    '''
    user = models.ForeignKey(User)
    group = models.ForeignKey('Group')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField()

    def __unicode__(self):
        return self.group.__unicode__() + " | " + self.user.__unicode__()
