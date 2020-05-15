from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView
from rest_framework import generics, permissions, status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, PostComment, Author
from .serializer import PostSerializers, CommentSerializer, RandomSerializer


@login_required
def like_disliked(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    print("Total", post.likes.count())
    url = reverse("post-detail", kwargs={"post_id": post.id})
    return HttpResponseRedirect(url)


class ArticleList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers


# operations with id
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers


@api_view(['GET', 'POST'])
def comment(request, pk):
    if request.method == 'GET':
        postcomment = PostComment.objects.filter(post=pk)
        commentserial = CommentSerializer(postcomment, many=True)
        return Response(commentserial.data)
    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def comment_update(request, ci):
    try:
        comment = PostComment.objects.get(id=ci)
    except:
        return
    if request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_required(IsAuthenticated)
@api_view(["GET", "POST"])
def like_dislike_api(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.is_authenticated():
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


