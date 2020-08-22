from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User as u, User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile, File, Follower
from .serializers import UserSerializer, ChangePasswordSerializer, FileSerializers, CurrentUserSerializers, \
    FollowingList
from post.serializer import PostSerializers


# for signup
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# for updating user's username
class UserUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


# for updating user's password
class UpdatePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# image based work
class UserProfilePicture(APIView):
    permission_classes = ([IsAuthenticated])
    parser_classes = ([MultiPartParser])

    def get(self, request):
        try:
            file = File.objects.get(user=request.user)
        except File.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        serial = FileSerializers(file)
        return Response(serial.data, status=status.HTTP_200_OK)

    def put(self, request):
        if 'file' not in request.data:
            raise Response(status=status.HTTP_204_NO_CONTENT)
        f = request.data['file']
        file1 = File.objects.get(user=request.user)
        file1.file = f
        file1.save()
        return Response(status=status.HTTP_201_CREATED)

    def post(self, request):
        if 'file' not in request.data:
            raise Response(status=status.HTTP_204_NO_CONTENT)
        f = request.data['file']
        file1 = File(user=request.user, file=f)
        file1.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        try:
            file = File.objects.get(user=request.user)
        except File.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# current user's post
class UserPostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            posts = self.request.user.posts
        except:
            Response({"error": "Data not found"}, status=status.HTTP_204_NO_CONTENT)

        serial = PostSerializers(posts, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


class CurrentUserDetail(APIView):
    permission_required = IsAuthenticated

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serial = CurrentUserSerializers(user)
        return Response(serial.data, status=status.HTTP_200_OK)


#
@api_view(['POST', 'PUT'])
# @permission_required([IsAuthenticated])
def followingfollow(request, pk):
    CurrentUser = User.objects.get(id=request.user.id)
    user = User.objects.get(id=pk)
    s = Follower.objects.create(following=user, follower=CurrentUser)
    CurrentUser.following.add(s)
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
def followinglist(request):
    s = request.user.following.all().values()
    print(list(s))
    l = []
    for i in list(s):
        print(i["following_id"])
        l.append(i["following_id"])
    return JsonResponse({
        'following': l
    })


@api_view(["GET"])
def followerlist(request):
    s = request.user.followers.all().values()
    print(list(s))
    l = []
    for i in list(s):
        print(i["follower_id"])
        l.append(i["follower_id"])
    return JsonResponse({
        'followers': l
    })


def home(request):
    user = User.objects.get(id=1)
    print(user)
    return render(request, "user/home.html", {'user': user})
