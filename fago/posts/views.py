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
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin


# Create your views here.
def home(request):
    posts = Post.objects.order_by('-posted_at')
    context = {
        'posts': posts,
    }
    return render(request, "posts/index.html", context=context)

# Implementation of class based views in cbv_branch

# Create post Class Based View
class CreatePostView(View):
    form_class = CreatePostForm # Form class that will be used to display the form
    template_name = 'posts/create_post.html' # Template that will be rendered
    
    """
    get method handles all the get request
    in this case the get methods renders the CreatePostForm on create_post.html
    """
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})
    
    """
    post method handels all the POST requests
    in this method it handels the data that the form will get as the post request
    """
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        passing the user as **kwargs in form
        check posts/forms.py CreatePostForm for further refrence
        """
        form = self.form_class(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post Created!")
            return redirect('read-post', post_id=post.id)
        
        return render(request, self.template_name, {'form': form})
    

# Read post Class Based View
class ReadPostView(DetailView, FormMixin):
    model = Post
    template_name = 'posts/read_post.html'
    context_object_name = 'post'
    # the id that the class will look for in the url
    pk_url_kwarg = 'post_id'

    form_class = CommentForm
    success_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = Comment.objects.filter(post=post).order_by('-comment_at')
        context['comments'] = comments
        # Because we need to pass the form in the get request too
        context['form'] = self.get_form()            
        return context
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.comment_author = request.user
            comment.save()
            messages.success(request, "Comment Added!")
            return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse('read-post', kwargs={'post_id': self.object.id})


# delete post
@login_required
def delete_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)

    if user == post.author:
        post.delete()
        messages.success(request, 'Post Deleted!')
        return redirect('home')
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