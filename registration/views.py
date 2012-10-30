from django.shortcuts import render_to_response, get_list_or_404, redirect
from forms import (
    LoginForm,
    RegistrationForm
)

def login(request):
    form = LoginForm()
    return render_to_response('prototype/login.html', {'form': form,});

def register(request):
    form = RegisterForm()
    return render_to_response('prototype/register.html', {'form': form,})
