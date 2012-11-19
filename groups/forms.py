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

    class Meta:
        model = Group
        fields = ('name',)
