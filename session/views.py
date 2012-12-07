from django.shortcuts import (
        render,
        get_list_or_404, 
        redirect
)
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import (
        authenticate,
        login,
        logout,
)

from registration.forms import (
    RegistrationForm
)
from django.utils.translation import ugettext, ugettext_lazy as _
from forms import LoginForm

def _login_form(request, state=""):
    return render(request, 'landing_page.html', {'state': state,
                                             'form': RegistrationForm()})

def login_view(request):

    if request.user.is_authenticated():
        if request.user.is_active:
            return render(request, 'inbox.html', {'user': request.user})
        else:
            return _login_form(request)

    state = ''
    if request.method == 'POST':
        if not request.session.test_cookie_worked():
            state = 'Please enable cookies'
            return _login_form(request, state)

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'inbox.html', {'user': user,})
            else:
                state = 'User not active. ' \
                        'Please check your email for validation'
        else:
            state = 'Invalid email or password. ' \
                    'Do you want to <a href=\"/reset_password/\">reset your password</a>?'

    request.session.set_test_cookie()
    return _login_form(request, state)

def logout_view(request):
    logout(request)
    return redirect('/')
