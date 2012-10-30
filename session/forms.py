from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=40, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True, max_length=40)
