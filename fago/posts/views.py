from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, CommentForm
from .models import Post, Comment

# Create your views here.
def home(request):
    posts = Post.objects.order_by('-posted_at')
    context = {
        'posts': posts
    }
    return render(request, "posts/index.html", context=context)

# Create Post Form
@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post Created!')
            return redirect('home')
    else:
        form = CreatePostForm(user=request.user)    
    context = {
        'form': form
    }
    
    return render(request, 'posts/create_post.html', context=context)

# Read a post
"""
Also handles the comment logic
"""
def read_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # checking the type of request for comment
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.comment_author = request.user
            comment.save()
            messages.info(request, 'Comment Added!')
            return redirect('read-post', post_id=post.id)
    else:
        form = CommentForm()
    
    comments = Comment.objects.filter(post=post).order_by('-comment_at').all()
    context = {
        'post':post,
        'comments':comments,
        'form': form,
    }

    return render(request, 'posts/read_post.html', context=context)