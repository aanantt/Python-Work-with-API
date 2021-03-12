from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from .models import Post, PostComment, PostImage
from .serializer import PostSerializers, CommentSerializer, PostImageSerializer


# @permission_required([IsAuthenticated])
# @login_required
@api_view(['POST'])
def like_disliked(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        return Response({'message': 'Like Removed'}, status=status.HTTP_200_OK)
    post.likes.add(user)
    return Response({'message': 'Liked'}, status=status.HTTP_200_OK)


class Comments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        post = Post.objects.get(id=id)
        post_comment = PostComment.objects.filter(post=post)
        comment_serial = CommentSerializer(post_comment, many=True)
        return Response(comment_serial.data)

    def post(self, request, id):
        print(f"Req{request.data.get('body')}")
        post = Post.objects.get(id=id)
        PostComment(body=request.data.get('body'), post=post, user=request.user).save()
        # serializer = CommentSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        comment = PostComment.objects.filter(id=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCreate(APIView):
    permission_required = IsAuthenticated
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        images = dict(request.data.lists())["post_image"]
        task = Post.objects.create(text=request.data['text'], author=request.user)
        for image_data in images:
            # ext = str(image_data).split('.')[-1]
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


@api_view(['GET'])
def userallpost(request, pk):
    user = User.objects.get(id=pk)
    posts = Post.objects.filter(author=user)
    if posts:
        post_serializers = PostSerializers(posts, many=True)
        return Response(post_serializers.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def currentuserallpost(request):
    user = User.objects.get(id=request.user.id)
    posts = Post.objects.filter(author=user)
    if posts:
        post_serializers = PostSerializers(posts, many=True)
        return Response(post_serializers.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_204_NO_CONTENT)


class PostImageList(APIView):
    permission_required = IsAuthenticated

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        images = post.images.all()
        serial = PostImageSerializer(images, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)
