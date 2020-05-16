from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Post, PostComment, PostImage
from .serializer import PostSerializers, CommentSerializer, PostImageSerializer


@permission_required([IsAuthenticated])
@login_required
def like_disliked(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        return Response("{'message':'Like Removed'}", status=status.HTTP_200_OK)
    post.likes.add(user)
    return Response("{'message':'Liked'}", status=status.HTTP_200_OK)


class Comments(APIView):
    permission_classes = IsAuthenticated

    def get(self, request, pk):
        post_comment = PostComment.objects.filter(post=pk)
        comment_serial = CommentSerializer(post_comment, many=True)
        return Response(comment_serial.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        comment = PostComment.objects.filter(post=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCreate(APIView):
    permission_required = IsAuthenticated
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        images = dict(request.data.lists())["post_image"]
        task = Post.objects.create(text=request.data['text'], author=request.user)
        for image_data in images:
            PostImage.objects.create(post=task, files=image_data)
        else:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostList(generics.ListAPIView):
    permission_required = IsAuthenticated
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class PostRUD(generics.RetrieveUpdateDestroyAPIView):
    permission_required = IsAuthenticated
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class PostImageList(APIView):
    permission_required = IsAuthenticated

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        images = post.images.all()
        serial = PostImageSerializer(images, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
