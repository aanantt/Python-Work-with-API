from time import timezone

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from django.db import models
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from post.models import UserFollowing
from .models import Story
from .serializer import StorySerializer


class CurrentUserStoryAPI(APIView):
    permission_required = [IsAuthenticated]

    def get(self, request):
        story = Story.objects.filter(author=self.request.user)
        if story:
            storySerial = StorySerializer(story, many=True)
            return Response(storySerial, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        # upload to firebase
        Story(path='\path',
              author=request.user,
              isImage=self.request.data.get("isImage")
              ).save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self, request, id):
        story = Story.objects.get(id=id, author=self.request.user)
        story.isSeen = True
        story.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id):
        story = Story.objects.get(id=id, author=self.request.user)
        story.delete()
        return Response(status=status.HTTP_200_OK)


# @api_view(["GET"])
# def getFollowingStory(request):
#     following = request.user.following.all()
#     stories = []
#     for i in following:



