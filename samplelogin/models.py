from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User as u
from django.db import models


class User(AbstractBaseUser):
    followers = models.ManyToManyField('self', related_name='follower', blank=True)
    following = models.ManyToManyField('self', related_name='following', blank=True)
    name = models.CharField(max_length=200)


class UserProfile(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="userprofile/", max_length=200, default="userprofile/avatar.png")


class File(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE, default="userprofile/user.jpeg")
    file = models.FileField(blank=False, null=False)
