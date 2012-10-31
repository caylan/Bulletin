from django.shortcuts import (
        render_to_response, 
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
from django.utils.translation import ugettext, ugettext_lazy as _
from forms import LoginForm

def _login_form(state=""):
    return render_to_response('login.html', {'state': state,
                                             'form': LoginForm()})

def login_view(request):

    if request.user.is_authenticated():
        if request.user.is_active:
            return render_to_response('index.html', {'user': request.user})
        else:
            return _login_form()

    if request.method == 'POST':
        if not request.session.test_cookie_worked():
            state = 'Please enable cookies'
            return _login_form(state)

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render_to_response('index.html', {'user': user,})
            else:
                state = 'User not active. ' \
                        'Please check your email for validation'
        else:
            state = 'Invalid email or password.'

        request.session.set_test_cookie()
        return _login_form(state)

    request.session.set_test_cookie()
    return _login_form()

def logout_view(request):
    logout(request)
    return redirect('/')
