from django.shortcuts import render_to_response, get_list_or_404
from prototype.models import Post, Comment

def index(request):
    return render_to_response('prototype/index.html')

def group(request, grpid):
    post_list = get_list_or_404(Post, group=grpid)
    return render_to_response('prototype/group.html', {'post_list': post_list, 'grpid': grpid})
