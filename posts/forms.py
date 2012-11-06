from django import forms
from models import Post

class PostForm(forms.ModelForm):
    """
    Form for the post model
    """
    message = forms.RegexField(regex=r'[^\s]',)

    class Meta:
        model = Post
        # the following should be set by the view depending on context
        exclude = ['author', 'group',]
