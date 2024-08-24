from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


# User Registration Form
"""
Declaring a UserRegistration Class which inherits from UserCreationForms
"""
class UserRegistrationForm(UserCreationForm):

    first_name = forms.CharField(label='Display Name:',max_length=50, required=True)

    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'first_name','email', 'password1', 'password2']


# User Login Form

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    
    first_name = forms.CharField(max_length=50)

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'profile_bio']
    
    """
    using the __init__ method we set up firstname field of the form the firstname of the current user.
    """
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name

    
    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        if commit:
            profile.user.save()
            profile.save()
        return profile
