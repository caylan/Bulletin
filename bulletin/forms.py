from django.contrib.auth.forms import UserCreationForm

class BulletinUserCreationForm(UserCreationForm):
    '''
    This will create a user once all of the criteria
    has been met.

    For now, the only forced criteria are that the email is required,
    but it should also require the first and last name.
    '''
    
    def __init__(self, *args, **kwargs):
        super(BulletinUserCreationForm , self).__init__(*args, **kwargs)

        self.fields['email'].required = True
