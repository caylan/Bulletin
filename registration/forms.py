from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    '''
    A form that creates a user, using all of the required
    fields.
    '''
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def clean_email(self):
        ''' Checks to see if a user with the following email exists '''
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email is registered. "
                                        "Did you forget your password?")
        except User.DoesNotExist:
            return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]
        user.is_active = False # false until email is activated!
        if commit:
            user.save()
        return user
