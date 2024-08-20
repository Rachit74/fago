from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=settings.PROFILE_PICS_DIR, blank=True, null=True)