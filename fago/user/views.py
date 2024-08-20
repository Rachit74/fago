from django.shortcuts import render
from .forms import UserRegistrationForm

# Create your views here.

user = {
    'id': 'useruuid',
    'username': 'user',
    'name': 'Test User',
    'bio': 'lorem ispum lorem ispum lorem ispum lorem ispum lorem ispum lorem ispum lorem ispum'
}

def user_profile(request):
    context = {
        'user':user
    }

    return render(request, 'user/profile.html', context=context)

# User Registration
def register_user(request):
    form = UserRegistrationForm()

    context = {
        'form':form
    }
    return render(request, 'user/register.html', context=context)