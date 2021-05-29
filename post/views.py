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
import json
from .models import Post, PostComment, PostImage, PostReply
from .serializer import PostSerializers, CommentSerializer, PostImageSerializer, ReplySerializer

import pyrebase

# for signup
conf = ''
# with open("/home/anant/PycharmProjects/API/Django/firebase.json") as f:
#     conf = f.read()
with open("/home/anant/PycharmProjects/API/Django/firebase.json", "r") as read_file:
    j = json.load(read_file)
# j = json.loads("/home/anant/PycharmProjects/API/Django/firebase.json")

config = j
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


# @permission_required([IsAuthenticated])
# @login_required
@api_view(['POST', 'PUT'])
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


class Reply(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        post = PostComment.objects.get(id=id)
        post_comment = PostReply.objects.filter(comment=post)
        comment_serial = ReplySerializer(post_comment, many=True)
        return Response(comment_serial.data)

    def post(self, request, id):
        print(f"Req{request.data.get('body')}")
        post = PostComment.objects.get(id=id)
        PostReply(body=request.data.get('body'), comment=post, user=request.user).save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        comment = PostReply.objects.filter(id=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCreate(APIView):
    permission_required = IsAuthenticated
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        images = dict(request.data.lists())["post_image"]
        print(images)
        task = Post.objects.create(text=request.data['text'], author=request.user)
        # USE models.ImageField IF YOU HAVE AWS, GCP or Azure, right now Iam using Firebase storage
        # so I will store file name as string in database and file in firebase storage

        # NOTE: Never use this Method in Production mode. It's highly insecure because we can access these files
        # in frontend without any authentication

        # I didn't find any proper documentation for Using Firebase storage with Django Media Files
        # that's why I am using this logic
        for image_data in images:
            print(image_data)
            file_ext = str(image_data).split('.')[1]
            import datetime
            file_name = str(self.request.user.id) + "__" + \
                        str(datetime.datetime.now().isoformat()) + "." + file_ext
            storage.child("file_data/" + file_name).put(image_data)
            PostImage.objects.create(post=task, files=f"files/{file_name}")
        return Response(status=status.HTTP_201_CREATED)


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
