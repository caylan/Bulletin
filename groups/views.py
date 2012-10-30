from django.shortcuts import render_to_response, get_list_or_404, redirect
from django.contrib.auth.models import User
from posts.models import Post, Comment
import md5

def index(request):
    try:
        user_id = request.session['user_id']
    except KeyError:
        pass
    return render_to_response('index.html', {'user_id': user_id})

def group(request, grpid):
    '''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(author=form.cleaned_data['author'],
                        message=form.cleaned_data['message'],
                        group=grpid)
            post.save()
            
            return redirect(group, grpid)
    else:
        form = PostForm()

                                                       'form': form})
    '''
    # post_list = get_list_or_404(Post, group=grpid)
    post_list = list(Post.objects.filter(group=grpid))
    return render_to_response('group.html', {'post_list': post_list,
                                                       'grpid': grpid,})
