from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

# User Registration Form
"""
Declaresa a UserRegistration Class which inherits from UserCreationForms

"""
class UserRegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user)
            if self.cleaned_data.get('profile_picture'):
                user_profile.profile_picture = self.cleaned_data['profile_picture']
                user_profile.save()
            
        return user
