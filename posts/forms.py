from django.forms import ModelForm
from models import Post

class PostForm(ModelForm):
    """
    Form for the post model
    """
    class Meta:
        model = Post
        # the following should be set by the view depending on context
        exclude = ['author', 'group',]
