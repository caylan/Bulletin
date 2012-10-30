from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class LoginForm(forms.Form):
    error_messages = {
        'invalid' : _("Invalid user name or password"),
    }
    email = forms.CharField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        fields = ('email', 'password')

    def clean_user(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            if user.check_password(self.cleaned_data['password']):
                return user
        except User.DoesNotExist:
            pass
        raise forms.ValidationError(self.error_messages['invalid'])
