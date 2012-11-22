from django.contrib.auth.models import User
from django.http import (
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from django.shortcuts import render
from forms import CommentForm, PostForm
from models import Comment, Post
from groups.models import Group
from gevent.event import AsyncResult

class Posts(object):
    def __init__(self):
        # map group.pk -> AsyncResult
        self.group_event = dict([])

    def comment(self, request, postid):
        '''
        make a comment for given post and render
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
                try:
                    comment_post = Post.objects.get(pk=postid)
                except DoesNotExist:
                    return HttpResponseNotFound()
                comment.post = comment_post
                comment.save()
                
                # is anybody listening in this group?
                # if so, set AsyncResult to comment and alert those listening
                # then delete the AsyncResult
                grpid = comment_author.group.pk
                if grpid in self.group_event:
                    self.group_event[grpid].set(comment)
                    del self.group_event[grpid]
                
                #return HttpResponse(comment.json(), mimetype='application/json')
                return render(request, 'group_comment.html', {'comment': comment})
        return HttpResponseBadRequest()

    def post(self, request, grpid):
        '''
        make a post for given group and render
        '''
        try:
            post_author = request.user.membership_set.get(group__pk=grpid)
        except:
            return HttpResponseForbidden

        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                # author = from the current user's set of memberships, the one that
                #          has a group with matching group id (pk)
                post.author = post_author
                post.save()

                # is anybody listening in this group?
                # if so, alert them
                if grpid in self.group_event:
                    self.group_event[grpid].set(post)
                    del self.group_event[grpid]

                #return HttpResponse(post.json(), mimetype='application/json')
                return render(request, 'group_post.html', {'post': post})
        return HttpResponseBadRequest()

    def update(self, request, grpid):
        '''
        wait until a post or comment has been made
        '''
        # are there already people waiting in this group?
        # if not, start an AsyncResult!
        if grpid not in self.group_event:
            self.group_event[grpid] = AsyncResult()
        # wait for something to get posted
        result = self.group_event[grpid].get()

        # got something, check type
        if type(result) is Post:
            return render(request, 'group_post.html', {'post': post})
        elif type(result) is Comment:
            return render(request, 'group_comment.html', {'comment': comment})
        else:
            # wasn't a post or comment, wonder how that happened...
            return HttpResponseServerError()

posts = Posts()
comment = posts.comment
post = posts.post
update = posts.update