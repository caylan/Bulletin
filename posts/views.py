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

class Posts(object):
    def __init__(self):
        pass

    def comment(self, request, grpid, postid):
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
                comment.post = Post.objects.get(pk=postid)
                comment.save()
                return HttpResponse(comment.json(), mimetype='application/json')
        return HttpResponseBadRequest()

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
post = posts.post