from django.contrib.auth.forms import UserCreationForm

class BulletinUserCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(BulletinUserCreationForm , self).__init__(*args, **kwargs)

        self.fields['email'].required = True
