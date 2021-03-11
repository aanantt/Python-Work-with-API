from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import UserProfile, File, Check, UserFollowing



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class FollowS(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CurrentUserSerializers(serializers.ModelSerializer):
    avatar = serializers.CharField(source="userprofile.avatar")
    followers = FollowS(read_only=True, many=True)
    following = FollowS(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'avatar', 'username', 'followers', 'following', 'date_joined','email']


class FileSerializers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class CheckSeial(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
