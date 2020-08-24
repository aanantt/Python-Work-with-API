from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User as u
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="userprofile/", max_length=200, default="userprofile/avatar.png")


class File(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE, default="userprofile/user.jpeg")
    file = models.FileField(blank=False, null=False)


class Follower(models.Model):
    follower = models.ForeignKey(u, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(u, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')

    def __unicode__(self):
        return u'%s follows %s' % (self.follower, self.following)


class Check(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=200)
