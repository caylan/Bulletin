from django.test import TestCase
from django.utils import timezone
from posts.models import Post
from posts.models import Comment
from groups.models import Group
from django.contrib.auth.models import User


class GroupModelTest(TestCase):
    def test_post(self):
        post = Post()
        
        user = User.objects.create_user('Testy McTest', 'test@test.com', 'testpassword')
        user.save()
        
        group = Group()
        group.name = "Test Group"
        group.save()
        
        post.author = User.objects.get(id = user.id)
        post.message = "Testing321"
        post.group = Group.objects.get(id = group.id)

        post.save()
    
        test_post = Post.objects.get(id = post.id)
        
        self.assertEquals(test_post, post)
        self.assertEquals(test_post.author, User.objects.get(id = user.id))
        self.assertEquals(test_post.message, "Testing321")
        self.assertEquals(test_post.group, Group.objects.get(id = group.id))
   
        post.delete()
        group.delete()
        user.delete()
        
        
    def test_comment(self):
        comment = Comment()
        post = Post()
        
        user = User.objects.create_user('Testy McTest', 'test@test.com', 'testpassword')
        user.save()
        
        group = Group()
        group.name = "Test Group"
        group.save()
        
        post.author = User.objects.get(id = user.id)
        post.message = "Testing 321"
        post.group = Group.objects.get(id = group.id)
        post.save()
        
        comment.author = User.objects.get(id = user.id)
        comment.message = " 123Testing"
        comment.group = Group.objects.get(id = group.id)
        comment.post = Post.objects.get(id = post.id)

        comment.save()
    
        test_comment = Comment.objects.get(id = post.id)
        
        self.assertEquals(test_comment, comment)
        self.assertEquals(test_comment.author, User.objects.get(id = user.id))
        self.assertEquals(test_comment.message, "Testing321")
        self.assertEquals(test_comment.group,  Group.objects.get(id = group.id))
   
        comment.delete()
        post.delete()
        group.delete()
        user.delete()
