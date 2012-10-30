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

    # If we have a cookie, redirect to main page.
    try:
        uid = request.session["user_id"]
        return render_to_response('index.html', {'user_id': request.session['user_id'],})
    except KeyError:
        pass

    valid = True
    cookies = True

    # If this was a post (they filled out the data), then redirect
    # them to the main page if valid.
    if request.method == 'POST':

        # If cookies are enabled, then check to see if the form is
        # valid.  If so, then redirect the user to the main page.
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            form = LoginForm(request.POST)

            # If the form was valid, then take the user to the main
            # login page iff their username exists, and their password
            # is valid.  If not, give them the invalid username/pass
            # page.
            if form.is_valid():
                try:
                    user = User.objects.get(email=request.POST['email'])
                    if user.check_password(request.POST['password']):
                        request.session["user_id"] = user.id
                        return render_to_response('index.html', {'user_id': request.session['user_id'],})
                except User.DoesNotExist:
                    pass
            valid = False
        else: # cookie was invalid.
            form = LoginForm()
            cookies = False
    else: # If this was a GET request. Give them the blank form.
        request.session.set_test_cookie()
        form = LoginForm()
    return render_to_response('login.html', {'form' : form, 'valid' : valid, 'cookies' : cookies})

def logout(request):
    '''
    This will log out the user, deleting their cookie (Eventually).
    For now we're not catching anything as we're hoping this will enforce
    logging out properly and cleanly.
    '''
    del request.session['user_id']
