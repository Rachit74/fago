from typing import Any
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
import json
# Form Imports
from .forms import CreatePostForm, CommentForm

# Model imports
from .models import Post, Comment, Notification
from communities.models import Community
from django.contrib.auth.models import User
from user.models import UserProfile
from django.db.models import Q

# Decorators import
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Class Based Views inheritance classes import
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin



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

        notification = Notification.objects.create(notification_type=2, from_user=self.request.user, to_user=post.author, post=post)

        messages.success(self.request, "Comment Added!")
        return redirect('read-post',post_id=post.id)
    


class PostLikeView(View):
  def post(self, request, post_id, *args, **kwargs):
    post = Post.objects.get(pk=post_id)
    
    is_dislike = False
    for dislike in post.dislikes.all():
      if dislike == request.user:
        post.dislikes.remove(request.user)
        break
    is_like = False
    for like in post.likes.all():
      if like == request.user:
        is_like = True
        break
    if not is_like:
      post.likes.add(request.user)
      notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)
    
    if is_like:
      post.likes.remove(request.user)

    next = request.POST.get('next')
    return HttpResponseRedirect(next, '/')

class PostDislikeView(View):
  def post(self, request, post_id, *args, **kwargs):
    post = Post.objects.get(pk=post_id)

    is_like = False
    for like in post.likes.all():
      if like == request.user:
        post.likes.remove(request.user)
        break
    is_dislikes = False
    for dislike in post.dislikes.all():
      if dislike == request.user:
        is_dislikes = True
        break
    if not is_dislikes:
      post.dislikes.add(request.user)
    if is_dislikes:
      post.dislikes.remove(request.user)

    next = request.POST.get('next')
    return HttpResponseRedirect(next, '/')


    
class PostNotificationView(View):
    def get(self, request, notification_id, post_id, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_id)
        post = Post.objects.get(pk=post_id)

        notification.user_has_seen = True
        notification.save()
        return redirect('read-post', post_id=post.id)

class CommentNotificationView(View):
    def get(self, request, notification_id, comment_id, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_id)
        comment = Comment.objects.get(pk=comment_id)

        notification.user_has_seen = True
        notification.save()
        return redirect('read-post', _id=comment.id)

class RemoveNotification(View):
    def delete(self, request, notification_id, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_id)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('success', content_type='text/plain')

# delete post
@login_required
def delete_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if not user == post.author:
        messages.error(request, 'Can not delete post!')
        return redirect('read-post', post_id=post.id)
    
    post.delete()
    messages.success(request, 'Post Deleted!')
    return redirect('user_profile')

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

class CommentReplyView(LoginRequiredMixin, FormView):
    template_name = 'posts/read_post.html'
    form_class = CommentForm
    login_url = 'login'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.parent_comment = get_object_or_404(Comment, id=self.kwargs['comment_id'])
        self.post = self.parent_comment.post
        return kwargs
    
    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.comment_author = self.request.user
        reply.parent_comment = self.parent_comment
        reply.post = self.post
        reply.save()

        messages.success(self.request, "Reply Added!")
        return redirect(reverse('read-post', kwargs={'post_id': self.post.id}))
        

class Search(View):
    """
    get function
    """
    def get(self, request):
        query = self.request.GET.get('query', '')

        users = User.objects.filter(Q(username__icontains=query))
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        communities = Community.objects.filter(Q(name__icontains=query))

        context = {
                'users':users,
                'posts':posts,
                'communities':communities,
                'query': query,
                }
        return render(self.request, 'posts/search.html', context=context)

