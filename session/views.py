from django.shortcuts import render_to_response, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from forms import LoginForm

__VALID__   = "You've logged in successfully!"

def login(request):
    '''
    This is a bit of a hack, but essentially we attempt to log in the
    user, and if they have an invalid password or email, then the
    form is labeled as invalid for the associated template.

    If the template is valid, then (for the moment) we create a user
    session and redirect them to a useless web page that doesn't do
    anything.
    '''
    valid = True
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=request.POST['email'])
                if user.check_password(request.POST['password']):
                    request.session["user_id"] = user.id
                    ''' This needs to send the user to the main page! '''
                    return HttpResponse(__VALID__)
                else:
                    valid = False
            except User.DoesNotExist:
                valid = False
                pass
        else:
            valid = False
    else:
        form = LoginForm()
    return render_to_response('login.html', {'form' : form, 'valid' : valid})
