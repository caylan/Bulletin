from django import forms
from models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Form for the post model
    """

    # Disallow anything that is only blank characters.
    message = forms.RegexField(regex=r'[^\s]',)

    class Meta:
        model = Post
        # the following should be set by the view depending on context
        exclude = ['author',]

class CommentForm(forms.ModelForm):
	"""
	Form for the comment model
	"""

	message = forms.RegexField(regex=r'[^\s]',)

	class Meta:
		model = Comment
		# the following should be set by the view depending on context
		exclude = ['author', 'post',]
