from django.shortcuts import render_to_response
from prototype.models import Post, Comment

def index(request):
    post_list = Post.objects.all()
    discussion = []
    for post in post_list:
        discussion.append((post, post.comment_set.all()))
    return render_to_response('prototype/index.html', {'discussion': discussion})
