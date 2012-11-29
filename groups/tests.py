from django.test import TestCase
from django.utils import timezone
from groups.models import Group
from groups.models import Membership
from django.contrib.auth.models import User
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "bulletin_project.settings"


class GroupModelTest(TestCase):
    def test_group(self):
        group = Group()
        group.name = "Test Group"

        group.save()
    
        test_group = Group.objects.get(id = group.id)
        
        self.assertEquals(test_group, group)
        self.assertEquals(test_group.name, "New Group")
        self.assertEquals(test_group.date_created, group.date_created)
   
        group.delete()
        
    
    def test_membership(self):
        membership = Membership()
        
        user = User.objects.create_user('Testy McTest', 'test@test.com', 'testpassword')
        user.save()
               
        group = Group()
        group.name = "Test Group"
        group.save()
        
        membership.user = User.objects.get(id = user.id)
        membership.group = Group.objects.get(id = group.id)
        membership.is_admin = False
         
        membership.save()
    
        test_membership = Membership.objects.get(id = membership.id)
        
        self.assertEquals(test_membership, membership)
        self.assertEquals(test_membership.user, User.objects.get(id = user.id))
        self.assertEquals(test_membership.group, Group.objects.get(id = group.id))
        self.assertEquals(test_membership.is_admin, False)
        
        membership.delete()
        group.delete()
        user.delete()