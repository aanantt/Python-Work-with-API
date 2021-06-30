from rest_framework import serializers
from .models import Story


class StorySerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        models = Story
        fields = ('id', 'author', 'isSeen', 'path', 'time', 'isImage')
