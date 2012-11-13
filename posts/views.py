from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.shortcuts import render
from forms import CommentForm
from models import Comment, Post
from groups.models import Group

@login_required
def comment(request, postid):
    post = Post.objects.get(pk=postid)
    # TODO check authorization

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # author = from the current user's set of memberships, the one that
            #          has a group with matching group id (pk)
            comment.author = request.user.membership_set.get(group__membership__post__pk=postid)
            # TODO try catch statement
            comment.post = Post.objects.get(pk=postid)
            comment.save()
            return HttpResponse(serializers.serialize('xml', [comment,]), mimetype='text/xml')
    else:
        return HttpResponseBadRequest()

@login_required
def delete_me(request):
    post_list = Post.objects.all()
    return render(request, 'delete_me.html', {'post_list': post_list,})