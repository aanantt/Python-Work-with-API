from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import datetime
# Create your models here.
from django.urls import reverse
from django.utils import timezone


# default=datetime.date.today
class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    post_image = models.ImageField(upload_to='postimages/', max_length=200, default="postimages/avatar.png")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
