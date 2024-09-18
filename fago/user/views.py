from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post

from django.views.generic import DetailView
from django.views.generic.edit import FormView

# Create your views here.

@login_required
def user_profile(request):

    user = request.user

    user_posts = Post.objects.filter(author=user)
    user_communities = user.communities.all()
    
    context = {
        'user':user,
        'user_posts': user_posts,
        'user_communities': user_communities,
    }

    return render(request, 'user/profile.html', context=context)

# Register User
class UserRegisterView(FormView):
    template_name = 'user/register.html'
    form_class = UserRegistrationForm

    def get_success_url(self):
        return reverse('user_profile')

    def form_valid(self, form: Any):
        user = form.save()
        UserProfile.objects.create(user=user)
        messages.success(self.request, "Account Created!")
        return HttpResponseRedirect(self.get_success_url())




# User Login
class LoginUserView(FormView):
    template_name = 'user/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse('user_profile')

    # form valid function
    def form_valid(self, form: Any):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user=user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form=form)


# User Logout
def logout_user(request):
    logout(request)

    messages.warning(request,"Logged Out!")
    return redirect('login')

# Edit User Profile
@login_required
def edit_user_profile(request):
    user = request.user
    """
    Before getting the user profile of any user we need to create their profile first
    which can be done using get_or_create()
    """
    # user_profile = UserProfile.objects.get(user=user) #this gives error as the user profile which is not created can not be extracted
    
    #get_or_create()
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if created:
        messages.info(request, "A new user profile was created")

    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated!")
            return redirect('user_profile')
    else:
        form = EditProfileForm(instance=user_profile)

    context = {
        'form': form
    }

    return render(request,'user/edit_profile.html', context=context)

# user profile view
class UserProfileView(DetailView):
    model = User
    template_name = 'user/oth_profile.html'
    context_object_name = 'user'

    # method used to overwrite what will be sent in the context
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_posts'] = Post.objects.filter(author=self.object)
        context['user_communities'] = self.object.communities.all()
        return context