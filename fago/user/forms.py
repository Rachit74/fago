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

    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# User Login Form

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'profile_bio']