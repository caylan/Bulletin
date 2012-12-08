from django.shortcuts import (
    render_to_response,
    get_list_or_404,
    redirect,
    render,
)
from django.template import RequestContext
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.forms.util import ErrorList
from models import (
    EmailConfirmationManager,
    EmailConfirmation,
    EmailInviteManager,
    EmailInvite,
)
from forms import (
    RegistrationForm, 
    InviteRegistrationForm,
    PasswordChangeForm,
)
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    Http404,
)
from django.conf import settings
from django.utils import simplejson
from django.contrib.auth.models import (
    User,
)
from groups.models import Group, Membership

def register(request):
    '''
    This handles the request sent to registration.  If the user
    has sent a confirmation to their email before, simply send another
    one.  
    
    This is to, hopefully, counteract the fact that people might
    have expired invitations in their inbox, or they deleted the confirmation
    email on accident.
    '''
    if request.user.is_authenticated():
        return render(request, 'register.html', {})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            ''' 
            We need to go to the email-sent page (even though an email
            isn't sent at the moment.
            '''
            user = form.save()
            EmailConfirmation.objects.send_confirmation(user=user)
            return render(request, 'email_sent.html', {'email': form.cleaned_data['email'] })
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form,})

def confirm_email(request, key):
    '''
    This confirms an email that has been sent by the website.
    This is strictly for email confirmations, not for invites from
    other users (those will be added later).
    '''
    confirmation_key = key.lower()
    user = EmailConfirmation.objects.confirm_email(key)
    params = {
        "user": user,
    }
    return render_to_response('confirm_email.html',
                              params,
                              context_instance=RequestContext(request))

def confirm_email_invite(request, key):
    '''
    Confirms an email invite to a specific user.  This may or may not redirect
    to a form for creating the new user (with first name, last name, and
    password).
    '''
    key = key.lower()
    user = EmailInvite.objects.confirm_email(key)
    if user is not None:
        # Handle the user case.
        if not user.is_active:
            '''
            This may not be the best idea, but if the user is not active, then
            activate them anyway, since this is just another link they'll have
            to follow if they haven't already.
            '''
            user.is_active = True

        # Check to see if they're already in the group, as this might not be the
        # first time they've visited this link.
        invite = EmailInvite.objects.get(confirmation_key=key)
        group = invite.group
        if not group.members.all().filter(email=user.email):
            # change invite to show that user accepted
            invite.acceptance = 'A'
            invite.save()
            #
            membership = Membership(user=user, group=group)
            membership.save()
            group.membership_set.add(membership)  # user is now a member!

        params = {
            'group': group,
            'user': user,
        }
        return render(request, 'invite_complete.html', params)
    else:
        # Handle the non-existing user case.
        recipient_email = EmailInvite.objects.get_email(key)
        if recipient_email is not None:
            # The email is not none, so now we need to create a user.
            # Redirect them to the form page for finishing their account.
            #
            # If they choose that they are an existing user, simply verify
            # their credentials and then add them to the group, redirecting
            # them to the inbox.
            return redirect('/invite_registration/{0}'.format(key))
        else:
            raise Http404

def invite_registration(request, key):
    '''
    Registers the user based on an their invitation.
    '''

    # If the email for this key doesn't exist, or there is a user already with
    # the email, then whoever is here is here for the wrong reason.  We'll (for
    # now) just give them a 404.
    email = EmailInvite.objects.get_email(key)
    if email is None:
        raise Http404
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None
    if user is not None:
        raise Http404

    # If we're here, we have a user's email, which will be used for creating the
    # user.
    if request.method == 'POST':
        form = InviteRegistrationForm(request.POST)
        if form.is_valid():
            '''
            If the form is all good and such, then send the user off to the page
            that'll say something like 'yay, you're registered with Bulletin!'
            '''
            user = form.save(email)
            invite = EmailInvite.objects.get(confirmation_key=key)
            # change invite to show that user accepted
            invite.acceptance = 'A'
            invite.save()
            #
            group = invite.group
            membership = Membership(user=user, group=group)
            membership.save()
            group.membership_set.add(membership)
            group.save()
            params = {
                'group': group,
                'user': user,
            }
            return render(request, 'invite_complete.html', params)
    else:
        form = InviteRegistrationForm()
    return render(request, 'register.html', {'form': form,})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        password_correct = False
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_pass = form.cleaned_data['new_password1']

            password_correct = request.user.check_password(current_password)
            if password_correct:
                request.user.set_password(new_pass)
                request.user.save()
                json = {'location': '.'}
                return HttpResponse(simplejson.dumps(json),
                    mimetype="application/json")

        if not password_correct:
            form._errors['current_password'] = ErrorList()
            form._errors['current_password'].append(_("Your password is incorrect"))
    else:
        raise Http404
    return render(request, 'password_change_modal.html', {'form': form})

def reset_password(request):
    '''
    Reset password for given email and send an email
    '''
    if request.method == 'POST':
        email = request.POST['email']
        try:
            forgetful_user = User.objects.get(email=email)
            new_password = User.objects.make_random_password()
            forgetful_user.set_password(new_password)
            forgetful_user.save()
            forgetful_user.email_user('[Bulletin] Password Reset', 
                    'New password: ' + new_password)
            return render(request, 'password_reset.html', {'password_changed': True,})
        except User.DoesNotExist:
            return render(request, 'password_reset.html', {'state': 'We have no record of that email address',})
    else:
        return render(request, 'password_reset.html')
