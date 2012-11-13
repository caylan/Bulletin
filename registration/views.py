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
    Confirms an email invite to a specific user.
    '''
    pass
