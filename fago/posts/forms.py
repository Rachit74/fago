from django import forms
from .models import Post

# Post Form
class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']