from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreatePostForm, CommentForm
from .models import Post, Comment, Notification

# Create your views here.
def home(request):
    posts = Post.objects.order_by('-posted_at')
    context = {
        'posts': posts,
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

            # send notification
            post_author = comment.post.author
            notification_from = comment.comment_author
            notification = Notification.objects.create(user=post_author, message=f"from  {comment.comment[0:20]}", notification_from=notification_from, post=post)
            notification.save()

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

    if user == comment.comment_author:
        comment.delete()
        messages.success(request, 'Comment deleted')
        return redirect('read-post', post_id=comment.post.id)
    else:
        messages.error(request, 'Can not delete comment!')
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

           # Send notification
            comment_author = parent_comment.comment_author
            notification_from = reply.comment_author
            Notification.objects.create(
                user=comment_author,
                message=f"{reply.comment[:20]}",  # Truncate the comment for brevity
                notification_from=notification_from,
                comment = parent_comment
            ).save()
            messages.success(request, 'Comment Added!')
            return redirect('read-post', post_id=post.id)
    else:
        form = CommentForm()
    
# Delete Notification view
@login_required
def delete_notification(request, notification_id):
    user = request.user
    notification = get_object_or_404(Notification, id=notification_id)
    if notification.user == user:
        notification.delete()
    else:
        messages.error("Can not delete notification")
    
    return redirect('home')

@login_required
def view_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    if notification.user != request.user:
        messages.error(request, "You do not have permission to view this notification.")
        return redirect('home')

    post = notification.post
    comments = []

    # If the notification is about a comment, get the comment and its replies
    if notification.comment:
        comment = notification.comment
        comments = comment.subcomments.all()
    else:
        comment = None

    context = {
        'post': post,
        'comment': comment,
        'comments': comments,
    }

    return render(request, 'posts/notification.html', context=context)