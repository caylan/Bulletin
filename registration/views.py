from django.shortcuts import (
    render_to_response,
    get_list_or_404,
    redirect,
    render,
)
from django.template import RequestContext
from models import (
    EmailConfirmationManager,
    EmailConfirmation,
    EmailInviteManager,
    EmailInvite,
)
from forms import RegistrationForm

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
        if user.is_active:
            #
            pass
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
            pass
        else:
            pass # Return a 404.
