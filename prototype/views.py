from django.shortcuts import render_to_response, get_list_or_404
from prototype.models import Post, Comment

def index(request):
    """
    post_list = Post.objects.all()
    discussion = []
    for post in post_list:
        discussion.append((post, post.comment_set.all()))
    return render_to_response('prototype/index.html', {'discussion': discussion})
    """
    return render_to_response('prototype/index.html')

def group(request, grpid):
    post_list = get_list_or_404(Post, group=grpid)
    return render_to_response('prototype/group.html', {'post_list': post_list, 'grpid': grpid})
