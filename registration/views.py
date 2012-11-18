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
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
from django.conf import settings

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
    key = key.lower()
    # user = EmailInvite.objects.confirm_email(key)
    if user.is_active:
        pass # If the user is active, show some banner or indication that
             # they're part of the new group.
    else:
        pass # If the user is not active, create a registration form for the
             # user and then have them fill out their name and password.

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

    def json_response(success, error=""):
        json_text = '{{ \
                    "success": {0}, \
                    "error": {1} \
                }}'.format(success, error)
        return HttpResponse(json_text, mimetype='application/json')

    if request.method == 'POST':
        cur_password = request.POST['cur_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not cur_password or not new_password1 or not new_password2:
            # a field wasn't filled
            return json_response(False, "Please fill all fields")

        if not request.user.check_password(cur_password):
            # incorrect password
            return json_response(False, "Incorrect password")

        if len(new_password1) < settings.MIN_PASSWORD_LEN or len(new_password2) < settings.MIN_PASSWORD_LEN:
            # new password too short
            return json_response(False, "New password must be at least {0} \
                    characters".format(settings.MIN_PASSWORD_LEN))

        request.user.set_password(new_password1)
        request.user.save()

        return json_response(True)
    else:
        return HttpResponseBadRequest()
