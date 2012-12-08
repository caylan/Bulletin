from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.shortcuts import render
from forms import CommentForm, PostForm
from models import Comment, Post
from groups.models import Group
from gevent import event as gevent
from inbox_notifications.views import notifications
import time

class PostViews(object):
    '''
    PostViews: python object to hold posting related post_views
    
    The reason this is all wrapped up in a class, instead of just module of
    def's, is for keeping track of a dictionary of events (group_event) in
    which all users have access to.
    
    So that it appears to be a typical views.py module, located at the bottom
    are variables called by the urlpatterns.

    Based on example from
    https://github.com/SiteSupport/gevent/tree/master/examples/webchat
    '''
    def __init__(self):
        # map grpid -> gevent.AsyncResult()
        self.group_event = dict([])

    def comment(self, request, postid):
        '''
        make a comment for given post and render
        '''
        time.sleep(1)
        # comfirm current user is a member of the group the post belongs to
        try:
            # author = the membership whose group has a membership with the post we're looking at
            comment_author = request.user.membership_set.get(group__membership__post__pk=postid)
        except:
            return HttpResponseForbidden()

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                # author = the membership whose group has a membership with the post we're looking at
                comment.author = comment_author
                try:
                    comment_post = Post.objects.get(pk=postid)
                except DoesNotExist:
                    return HttpResponseNotFound()
                comment.post = comment_post
                comment.save()
                # is anybody listening?
                # if so, send new comment to everyone and reset
                grpid = int(comment_post.author.group.pk)
                if grpid in self.group_event:
                    self.group_event[grpid].set(comment)
                    # self.group_event = None
                    del self.group_event[grpid]
                return render(request, 'group_comment.html', {'comment': comment})
        return HttpResponseBadRequest()

    def post(self, request, grpid):
        '''
        make a post for given group and render
        '''
        time.sleep(1)
        try:
            post_author = request.user.membership_set.get(group__pk=grpid)
        except:
            return HttpResponseForbidden()

        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                # author = from the current user's set of memberships, the one that
                #          has a group with matching group id (pk)
                post.author = post_author
                post.save()
                # is anybody listening?
                # if so, send new post to everyone and reset
                grpid = int(grpid)
                if grpid in self.group_event:
                    self.group_event[grpid].set(post)
                    # self.group_event = None
                    del self.group_event[grpid]
                return render(request, 'group_post.html', {'post': post})
        return HttpResponseBadRequest()

    def update(self, request, grpid):
        '''
        wait until a post or comment has been made, render and return it
        '''
        grpid = int(grpid)
        if grpid not in self.group_event:
            self.group_event[grpid] = gevent.AsyncResult()
        update_content = self.group_event[grpid].get()
        if type(update_content) is Comment:
            return render(request, 'group_comment.html', {'comment': update_content})
        elif type(update_content) is Post:
            return render(request, 'group_post.html', {'post': update_content})
        else:
            # i have no idea how this happened
            return HttpResponseServerError("unhandled return type: {0}".format(type(update_content)))

# called by the urlpatterns
post_views = PostViews()
comment = post_views.comment
post = post_views.post
update = post_views.update
