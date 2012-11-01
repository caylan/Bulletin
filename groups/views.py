from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext, ugettext_lazy as _
from posts.models import Post, PostForm, Comment
import md5

@login_required
def index(request):
    return render(request, 'index.html', {'user': request.user})

@login_required
def group(request, grpid):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.group = grpid
            post.save()
            return HttpResponseRedirect("")
        # else, form not valid, return with errors
    else:  # not POST, so give a form with some prepopulated stuff
        form = PostForm()
    # list containin posts in order specified by post model
    post_list = list(Post.objects.filter(group=grpid))
    return render(request, 'group.html', {'post_list': post_list,
                                          'grpid': grpid,
                                          'user': request.user,
                                          'form': form})

