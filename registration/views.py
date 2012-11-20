from django.shortcuts import (
    render_to_response,
    get_list_or_404,
    redirect,
    render,
)
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import (
    EmailConfirmationManager,
    EmailConfirmation,
    EmailInviteManager,
    EmailInvite,
)
from forms import RegistrationForm, InviteRegistrationForm
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    Http404,
)
from django.conf import settings
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
        group = EmailInvite.objects.get(confirmation_key=key).group
        if not group.members.all().filter(email=user.email):
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
            group = EmailInvite.objects.get(confirmation_key=key).group
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

def change_password(request):
    '''
    Handle password change logic
    returns JSON value True on success
    {
        "success": true/false,
        "error": "error message"
    }

    input: cur_password, new_password1, new_password2
    output: error messages
    '''
    if not request.user.is_authenticated():
        raise Http404

    '''
    TODO: This should most likely be a form and return HTTP instead of JSON for
    the form response.
    '''
    def json_response(success, error=""):
        json_text = '{{"success": {0}, "error": "{1}"}}'.format(success, error)
        return HttpResponse(json_text, mimetype='application/json')

    if request.method == 'POST':
        cur_password = request.POST['cur_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not cur_password or not new_password1 or not new_password2:
            # a field wasn't filled
            return json_response("false", "Please fill all fields")

        if not request.user.check_password(cur_password):
            # incorrect password
            return json_response("false", "Incorrect password")

        if len(new_password1) < settings.MIN_PASSWORD_LEN or len(new_password2) < settings.MIN_PASSWORD_LEN:
            # new password too short
            return json_response("false", "New password must be at least {0} characters".format(settings.MIN_PASSWORD_LEN))

        if new_password1 != new_password2:
            # password fields don't match
            return json_response("false", "New password fields must match")

        request.user.set_password(new_password1)
        request.user.save()

        return json_response("true")
    else:
        return HttpResponseBadRequest()

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
