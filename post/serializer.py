from rest_framework import serializers

from .models import Post, PostComment


class PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        include = 'comments'
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
