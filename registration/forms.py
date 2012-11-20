from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings

class __BaseRegistrationForm(forms.ModelForm):
    '''
    This is a basic form for implementing the user registration sans email,
    since the user is going to be creating their account for the first time on
    the website.
    '''
    error_messages = {
        'duplicate_email'    : _("A user with that email already exists"),
        'password_mismatch'  : _("The two passwords did not match"),
        'password_too_short' : _("Your password should be at least 6 characters."),
    }
    
    first_name = forms.RegexField(regex=r'^[\w.@+-]+$',
                                  widget=forms.TextInput(attrs={'placeholder': 'First Name'}), 
                                  max_length=40,
                                  required=True,
                                  label='')
    first_name.widget.attrs['class'] = 'input-block-level'
    
    last_name = forms.RegexField(regex=r'^[\w.@+-]+$',
                                 widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
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

    def clean_password1(self):
        cleaned_data = super(self.__class__, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if len(password1) < settings.MIN_PASSWORD_LEN:
            raise forms.ValidationError(self.error_messages['password_too_short'])
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        return password1

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password1', 'password2',)

class InviteRegistrationForm(__BaseRegistrationForm):
    '''
    This passes for now, but in case we want to have any custom init function,
    that's why there's this and the BaseRegistrationForm, so that it doesn't
    affect the main registration form.

    When the someone is using this form, it is assumed that they will have
    access to the user's email upon registering them.
    '''
    def save(self, email, commit=True):
        '''
        Saves the user with the email passed.  The email must be valid, else an
        exception will be raised.
        '''
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            raise Exception('user must not exist!')

        user = super(InviteRegistrationForm, self).save(commit=False)

        ''' Don't activate a user until the email is sent! '''
        user.set_password(self.cleaned_data["password1"])
        user.username = email
        user.email = email
        if commit:
            user.save()
        return user

class RegistrationForm(__BaseRegistrationForm):

    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email Address'}),
                             label='', 
                             max_length=40, 
                             required=True)
    email.widget.attrs['class'] = 'input-block-level'

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

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)
