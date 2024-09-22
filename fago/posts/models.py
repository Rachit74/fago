from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from communities.models import Community

# Create your models here.

# Post Model
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to=settings.POSTS_PICS_DIR,
                              blank=True,
                              null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(timezone.now, default=timezone.now)
    community = models.ForeignKey(Community, related_name='posts', on_delete=models.CASCADE, default=None, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    pinned = models.BooleanField(default=False)
    # archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    
# Comment Model
class Comment(models.Model):
    comment = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_at = models.DateTimeField(timezone.now, default=timezone.now)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_like')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislike')

    #self refrencial field parent for thread comments
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcomments')

    def __str__(self) -> str:
        return self.comment
    
    def is_parent(self):
        """
        returns True if the comment is a parent comment
        """
        return self.parent_comment is None


class Notification(models.Model):
    '''
    all the notifications type will be represented as integers:
    1 --> Like    notification
    2-- > Comment notification
    '''
    notification_type = models.IntegerField()
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_from', null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_to', null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)