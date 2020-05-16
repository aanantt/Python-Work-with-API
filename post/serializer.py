from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post, PostComment, PostImage


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    id = serializers.IntegerField(required=False)

    class Meta:
        model = PostComment
        fields = '__all__'

    def save(self, **kwargs):
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class PostSerializers(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    files = PostImageSerializer(source='postimage_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'likes', 'date_posted', 'files')
