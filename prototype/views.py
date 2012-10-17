from django.shortcuts import render_to_response
from prototype.models import Post, Comment

def index(request):
    post_list = Post.objects.all()
    return render_to_response('prototype/index.html', {'post_list': post_list})
