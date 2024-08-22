from django import forms
from .models import Post, Comment

# Post Form
class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

# Comment Form
class CommentForm(forms.ModelForm):
    
    comment = forms.CharField(
        widget = forms.Textarea(
            attrs = {
                'rows': 5,
        }
        )
    )

    class Meta:
        model = Comment
        fields = ['comment']