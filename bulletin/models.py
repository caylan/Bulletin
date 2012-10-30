from django.db import models
from django.contrib.auth.models import (
    User, Group
)

"""
This is where the basic user info is made.
"""

class BulletinUser(User):
    '''
    This is a custom class overriding the default class inherited
    from django.contrib.auth.models.User
    '''
    def is_in_group(self):
        return bool(self.groups.all())

    def is_group_admin(self, group):
        '''
        Determines if the user is the admin of a group.
        '''
        pass
