from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
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
            # author = the membership whose group has a membership with the post we're looking at
            comment.author = request.user.membership_set.get(group__membership__post__pk=postid)
            # TODO try catch statement
            comment.post = Post.objects.get(pk=postid)
            comment.save()
            return HttpResponse(comment.json(), mimetype='application/json')
    else:
        return HttpResponseBadRequest()

@login_required
def delete_me(request):
    post_list = Post.objects.all()
    return render(request, 'delete_me.html', {'post_list': post_list,})