from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User as u
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE)
    # USE models.ImageField IF YOU HAVE AWS, GCP or Azure, right now Iam using Firebase storage
    # so I will store file name as string in database and file in firebase storage

    # NOTE: Never use this Method in Production mode as it's highly insecure

    # I didn't find any proper documentation for Using Firebase storage with Django Media Files
    # that's why I am using this logic

    # avatar = models.ImageField(upload_to="userprofile/", max_length=200, default="userprofile/avatar.png")
    avatar = models.CharField(max_length=200)


class File(models.Model):
    user = models.OneToOneField(u, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False)


class FollowSystem(models.Model):
    pass


class UserFollowing(models.Model):
    follower_user_id = models.ForeignKey(u, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(u, related_name="followers", on_delete=models.CASCADE)


# class Follower(models.Model):
#     follower = models.ForeignKey(u, related_name='follower', on_delete=models.CASCADE)
#
#
# class Following(models.Model):
#     following = models.ForeignKey(u, related_name='following', on_delete=models.CASCADE)

# class Meta:
#     unique_together = ('follower', 'following')
#
# def __unicode__(self):
#     return u'%s follows %s' % (self.follower, self.following)


class Check(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=200)
