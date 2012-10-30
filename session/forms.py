from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password')

