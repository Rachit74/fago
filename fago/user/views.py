from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.

def user_profile(request):

    user = request.user
    
    context = {
        'user':user
    }

    return render(request, 'user/profile.html', context=context)

# User Registration
def register_user(request):
    # condition to check the type of request by the client
    if request.method == "POST":
        # get the user form data that was posted
        form = UserRegistrationForm(request.POST)
        #checks if the form is valid
        if form.is_valid():
            form.save()
            print("USER CREATED!")
    else:
        form = UserRegistrationForm()

    context = {
        'form':form
    }
    return render(request, 'user/register.html', context=context)

# User Login
def login_user(request):
    # check the type of request
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password = password)
            login(request, user)

            return redirect('user_profile')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context=context)

# Edit User Profile
def edit_user_profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return redirect('user_profile')
    else:
        form = EditProfileForm()

    context = {
        'form': form
    }

    return render(request,'user/edit_profile.html', context=context)