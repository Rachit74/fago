from django import forms
from .models import Post, Comment
from communities.models import Community

# Post Form
class CreatePostForm(forms.ModelForm):
    community = forms.ModelChoiceField(
        queryset=Community.objects.none(),
        label = 'Choose a community',
        widget=forms.Select
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'community']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)  # Call the parent class's __init__ method
        if user:
            # Filter communities to only those the user is a member of
            self.fields['community'].queryset = Community.objects.filter(members=user)

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