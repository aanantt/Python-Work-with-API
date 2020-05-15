from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from .models import Post, PostComment, Author


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    id = serializers.IntegerField(required=False)

    class Meta:
        model = PostComment
        fields = '__all__'

    def save(self, **kwargs):
        kwargs["user"] = self.fields["user"].get_default()
        return super().save(**kwargs)


class PostSerializers(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = '__all__'

    def save(self, **kwargs):
        kwargs["author"] = self.fields["author"].get_default()
        return super().save(**kwargs)

