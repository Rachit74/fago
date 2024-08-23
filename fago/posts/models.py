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

    def __str__(self) -> str:
        return self.title


# Comment Model
class Comment(models.Model):
    comment = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_at = models.DateTimeField(timezone.now, default=timezone.now)

    #self refrencial field parent for thread comments
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcomments')

    def __str__(self) -> str:
        return self.comment
    
    def is_parent(self):
        """
        returns True if the comment is a parent comment
        """
        return self.parent_comment is None