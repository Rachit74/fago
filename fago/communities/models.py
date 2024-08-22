from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

# Community Model
class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User, related_name='communities')

    def __str__(self) -> str:
        return self.name