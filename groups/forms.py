from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from models import Group
import re

class GroupCreationForm(forms.ModelForm):
    '''
    This for will create a group with the specified name.
    It is recommended that a user be able to invite other members
    to a group via the Membership model (in groups.models)
    '''
    name = forms.RegexField(regex=r'[^\s]',
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Group Name'}
                            ), 
                            required=True,
                            label='')

    def __init__(self, *args, **kwargs):
        try:
            emails = kwargs.pop('emails')
        except KeyError:
            emails = []
        super(GroupCreationForm, self).__init__(*args, **kwargs)

        # Deal with creating the extra email fields.  This will allow us to also
        # validate the emails on the backend.
        for name, email in emails:
            self.fields[str(name)] = forms.EmailField(
                widget=forms.TextInput(attrs={'placeholder': 'Email Address'}),
                label=email,
                max_length=40,
                required=True,
            )

    def emails(self):
        '''
        Returns an iterable list of pairs over which we will be able to traverse
        and get all of the emails we want.
        '''
        emails = []
        for name, value in self.cleaned_data.items():
            if re.match(r'^email\d+$', name):
                emails.append(value)
        return emails

    class Meta:
        model = Group
        fields = ('name',)
