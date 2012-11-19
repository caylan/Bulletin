from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext, ugettext_lazy as _
from forms import GroupCreationForm
from models import Group, Membership
from posts.forms import PostForm
from posts.models import Post, Comment
import re
import md5

@login_required
def index(request):
    return render(request, 'inbox.html', {'user': request.user})

@login_required
def group(request, grpid):
    
    # If the user viewing is not a member of this group,
    # tell them it's a 404.
    if not request.user.group_set.filter(id=grpid):
        raise Http404

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # author = from the current user's set of memberships, the one that
            #          has a group with matching group id (pk)
            post.author = request.user.membership_set.get(group__pk=grpid)
            post.save()
            return HttpResponseRedirect("")
    else:  # not POST, so give a form with some prepopulated stuff
        form = PostForm()

    '''relations are represented by double underscores (i heart django)'''
    post_list = list(Post.objects.filter(author__group__id=grpid))

    # Is the user an admin for this group?
    is_admin = request.user.membership_set.get(group__pk=grpid).is_admin
    return render(request, 'group_view.html', {'post_list': post_list,
                                          'grpid': int(grpid),
                                          'user': request.user,
                                          'form': form,
                                          'is_admin': is_admin})

def _get_extra_emails(request):
    '''
    Gets the extra emails from a request.  This is meant to be used with group
    creation for extracting a list of emails.
    '''
    emails = []
    for name, val in request.POST.iteritems():
        if re.match('email', name):
            print val
    return emails

@login_required
def create(request):
    '''
    Sets up a group creation form wherein the user may choose the necessary
    criteria for the group they wish to create.

    The user may select the name of the group.
    '''
    if request.method == 'POST':
        emails = _get_extra_emails(request)
        form = GroupCreationForm(request.POST, emails=emails)
        if form.is_valid():
            group = form.save()
            
            # Create the default user membership
            m = Membership(user=request.user, group=group, is_admin=True)
            m.save()

            ''' Redirect to the new group '''
            return HttpResponse(group.json(), mimetype='application/json')
    else:
        raise Http404
    return render(request, 'group_create_modal.html', {'form': form,})
