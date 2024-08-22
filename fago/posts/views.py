from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, "posts/index.html", context=context)

# Create Post Form
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post Created!')
            return redirect('home')
    else:
        form = CreatePostForm()    
    context = {
        'form': form
    }
    
    return render(request, 'posts/create_post.html', context=context)