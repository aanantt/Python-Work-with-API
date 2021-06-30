
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Story(models.Model):
    path = models.CharField(max_length=200)
    author = models.ForeignKey(User, related_name='author')
    time = models.DateTimeField(auto_now_add=True, default=timezone.now)
    isImage = models.BooleanField(default=True)
    isSeen = models.BooleanField(default=False)
