from django.shortcuts import render

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