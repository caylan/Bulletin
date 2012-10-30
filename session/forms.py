from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password')

