from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _

class RegistrationForm(forms.ModelForm):
    error_messages = {
        'duplicate_email'   : _("A user with that email already exists"),
        'password_mismatch' : _("The two passwords did not match"),
    }

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}),
                             label='', 
                             max_length=40, 
                             required=True)
    email.widget.attrs['class'] = 'input-block-level'
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}), 
                                 max_length=40,
                                 required=True,
                                 label='')
    first_name.widget.attrs['class'] = 'input-block-level'
    
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
                                max_length=40,
                                required=True,
                                label='')
    last_name.widget.attrs['class'] = 'input-block-level'
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), 
                                label='')
    password1.widget.attrs['class'] = 'input-block-level'
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                                label='')
    password2.widget.attrs['class'] = 'input-block-level'

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean_email(self):
        '''
        Check for a clean email.  If the user exists and is active, throw an
        exception (since this will mean there is a duplicate email in the database).

        If the user exists with the same email but is not active, then
        it's okay to send the confirmation email again because the account has never
        been activated in the first place.
        '''
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        if user.is_active:
            raise forms.ValidationError(self.error_messages['duplicate_email'])
        else:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        '''
        In this instance, the username is set to be the email,
        so that we don't have to worry about uniqueness.  This
        is indeed a little bit of a hack, so maybe this can be changed
        later by making a custom User class (like what was planned
        in the first place).

        If the user still exists but is not active, then we simply
        return the user again, since we're going to send another
        validation in the view.py method (at least, that's what we're supporting).
        '''
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            user = super(RegistrationForm, self).save(commit=False)
            user.username = self.cleaned_data['email']

        ''' Don't activate a user until the email is sent! '''
        user.is_active = False 
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
