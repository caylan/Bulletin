from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
)
from django.shortcuts import render
from forms import CommentForm, PostForm
from models import Comment, Post
from groups.models import Group
from gevent.event import Event

class Posts(object):
    def __init__(self):
        # map group.pk -> gEvent
        self.group_event = dict([])

    def comment(self, request, grpid, postid):
        '''
        make a comment for given post, return comment json
        '''

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
                comment.author = comment_author
                # TODO try catch statement
                comment_post = Post.objects.get(pk=postid)
                comment.post = comment_post
                comment.save()
                
                # is anybody listening in this group?
                # if so, alert them
                if postid in self.group_event and not self.group_event[postid].is_set():
                    self.group_event[postid].set()
                    self.group_event[postid].clear()
                
                return HttpResponse(comment.json(), mimetype='application/json')
        return HttpResponseBadRequest()

    def update(self, request, grpid):
        '''
        wait until a post or comment has been made
        '''
        pass

    @login_required
    def post(self, request, grpid):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                # author = from the current user's set of memberships, the one that
                #          has a group with matching group id (pk)
                post.author = request.user.membership_set.get(group__pk=grpid)
                post.save()
                return HttpResponse(post.json(), mimetype='application/json')
        return HttpResponseBadRequest()

posts = Posts()
comment = posts.comment
update = posts.update
post = posts.post