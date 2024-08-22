from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

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


# Comment Model
class Comment(models.Model):
    comment = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)