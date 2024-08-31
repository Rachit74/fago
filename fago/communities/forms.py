from django import forms
from .models import Community

# Create Commnity Form
class CreateCommunityForm(forms.ModelForm):
    
    class Meta:
        model = Community
        fields = ['name', 'description', 'banner']