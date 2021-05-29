from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post, PostComment, PostImage, PostReply


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReply
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    id = serializers.IntegerField(required=False)
    replies = ReplySerializer(many=True)  # ForeignKey vale ka related name aayega

    class Meta:
        model = PostComment
        fields = ('id', 'user', 'body', 'date_posted', 'replies')

    # def save(self, **kwargs):
    #     print(kwargs)
    #     kwargs["user"] = self.fields["user"].get_default()
    #     return super().save(**kwargs)


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    likes = serializers.CharField(source='user__username')

    class Meta:
        model = Post
        fields = ('likes',)


class PostSerializers(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    images = PostImageSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'likes', 'date_posted', 'images')
