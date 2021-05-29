from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    text = models.CharField(max_length=250, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)

    # def save(self, *args, **kwargs):
    #     super(Post, self).save(*args, **kwargs)


class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    # USE models.FileField IF YOU HAVE AWS, GCP or Azure, right now Iam using Firebase storage
    # so I will store file name as string in database and file in firebase storage

    # NOTE: Never use this Method in Production mode. It's highly insecure because we can access these files
    # in frontend without any authentication

    # I didn't find any proper documentation for Using Firebase storage with Django Media Files
    # that's why I am using this logic
    files = models.CharField(max_length=200)
    # files = models.FileField(upload_to='postimages/', blank=True)


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)


class PostReply(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='replies')
    body = models.CharField(
        max_length=250
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
