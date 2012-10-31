from django.shortcuts import render_to_response, get_list_or_404, redirect
from models import (
    EmailConfirmationManager,
    EmailInvite,
    EmailConfirmation,
    AbstractEmailConfirmation
)
from forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            ''' 
            We need to go to the email-sent page (even though an email
            isn't sent at the moment.
            '''
            form.save()
            return render_to_response('email_sent.html', {'email': form.cleaned_data['email'] })
    else:
        form = RegistrationForm()
    return render_to_response('register.html', {'form': form,})

def confirm_email(request, key):
    '''
    This confirms an email that has been sent by the website.
    This is strictly for email confirmations, not for invites from
    other users (those will be added later).
    '''
    confirmation_key = confirmation_key.lower()
    email = AbstractEmailConfirmation.objects.confirm_email(key)
    return render_to_response('confirm_email/(

