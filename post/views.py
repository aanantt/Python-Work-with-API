from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import generics, permissions, status, serializers
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, PostComment
from .serializer import PostSerializers, CommentSerializer


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


class ArticleList(generics.ListCreateAPIView):
    permission_required = AllowAny
    parser_classes = [MultiPartParser, FormParser,JSONParser]
    queryset = Post.objects.all()
    serializer_class = PostSerializers


# operations with id
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_required = IsAuthenticated
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    queryset = Post.objects.all()
    serializer_class = PostSerializers


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


class Posts(APIView):
    permission_required = IsAuthenticated
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        pass

    def get(self, request):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass
