from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

# Form Imports
from .forms import CreatePostForm, CommentForm

# Model imports
from .models import Post, Comment, Notification
from communities.models import Community
from django.contrib.auth.models import User
from django.db.models import Q

# Decorators import
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Class Based Views inheritance classes import
from django.views import View
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin


# Implementation of class based views in cbv_branch

# Home List view to list all posts
class HomeView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'


# Create Post view using CreateView class inheritance
class CreatePostView(LoginRequiredMixin, FormView):
    form_class = CreatePostForm
    template_name = 'posts/create_post.html'
    login_url = 'login'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['community'].queryset = Community.objects.filter(members=self.request.user)
        return form

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        messages.success(self.request, "Post Added!")
        return redirect('read-post', post_id=post.id)

class ReadPostView(FormView):
    template_name = 'posts/read_post.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs['post_id']
        comments = Comment.objects.filter(post=post_id)
        context['post'] = get_object_or_404(Post, id=post_id)
        context['comments'] = comments
        return context
    
    def form_valid(self, form: Any):
        if not self.request.user.is_authenticated:
            return redirect('login')
        
        post = self.get_context_data()['post']
        comment = form.save(commit=False)
        comment.comment_author = self.request.user
        comment.post = post
        comment.save()
        messages.success(self.request, "Comment Added!")
        return redirect('read-post',post_id=post.id)


# delete post
@login_required
def delete_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if user == post.author:
        post.delete()
        messages.success(request, 'Post Deleted!')
        return redirect('user_profile')
    else:
        messages.error(request, 'Can not delete post!')
        return redirect('read-post', post_id=post.id)

# delete comment
@login_required
def delete_comment(request, comment_id):
    user = request.user
    comment = get_object_or_404(Comment, id=comment_id)

    if not user == comment.comment_author:
        messages.error(request, "Can not delete someone else comment!")
        return redirect('read-post', post_id=comment.post.id)

    comment.delete()
    messages.success(request, 'Comment deleted')
    return redirect('read-post', post_id=comment.post.id)



@login_required
def comment_reply(request, comment_id):
    user = request.user
    parent_comment = get_object_or_404(Comment, id=comment_id)
    post = parent_comment.post

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment_author = user
            reply.post=post
            reply.parent_comment = parent_comment
            reply.save()

            # send notification
            comment_author = parent_comment.comment_author
            notification = Notification.objects.create(
                notification_for = comment_author,
                notification_from = reply.comment_author,
                comment = parent_comment,
                post = post
            )

            notification.save()

            messages.success(request, 'Comment Added!')
            return redirect('read-post', post_id=post.id)
    else:
        form = CommentForm()
    
# Delete Notification view
@login_required
def delete_notification(request, notification_id):
    user = request.user
    notification = get_object_or_404(Notification, id=notification_id)
    if notification.notification_for == user:
        notification.delete()
    else:
        messages.error("Can not delete notification")
    
    return redirect('home')

@login_required
def notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    if notification.notification_for != request.user:
        messages.error(request, "You do not have permission to view this notification.")
        return redirect('home')

    post = notification.post
    comment = notification.comment
    subcomments = notification.comment.subcomments.all()

    context = {
        'post': post,
        'comment': comment,
        'subcomments': subcomments,
    }

    return render(request, 'posts/notification.html', context=context)

# Search query view
def search(request):

    query = request.GET.get('query', '')


    users = User.objects.filter(Q(username__contains=query))
    posts = Post.objects.filter(Q(title__contains=query) | Q(content__contains=query))
    communities = Community.objects.filter(Q(name__contains=query))

    context = {
        'users': users,
        'posts': posts,
        'communities': communities,
    }

    return render(request, 'posts/search.html', context=context)