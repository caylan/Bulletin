from django.shortcuts import render_to_response, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import (
        authenticate,
        login,
        logout,
)
from django.utils.translation import ugettext, ugettext_lazy as _
from forms import LoginForm

def get_user_id(request):
    try:
        uid = request.session["user_id"]
    except KeyError:
        return None
    user = User.objects.get(id=uid)
    ret_str = "{0} {1} ({2})".format(user.first_name, \
                                     user.last_name, \
                                     user.email)
    return _(ret_str)

def _login_form(valid=True, cookies=True, active=True):
    return render_to_response('login.html', {'valid': valid,
                                             'active': active,
                                             'cookies': cookies,
                                             'form': LoginForm()})

def login_view(request):
    if request.user and request.user.is_active:
            return render_to_response('index.html')

    if request.method == 'POST':
        if not request.session.test_cookie_worked():
            return _login_form(cookies=False)
        request.session.delete_test_cookie()
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return render_to_response('index.html')
            else:
                return _login_form(active=False)
        else:
            return _login_form(valid=False)
    else:
        '''
        If the user exists in the cookies, then check to see if
        they're valid.  If so, redirect to the login page.
        '''
        request.session.set_test_cookie()
        return _login_form()

def logout_view(request):
    logout(request)
    return render_to_response('index.html')
