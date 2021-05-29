import datetime
import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User as u, User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from django.core import serializers
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile, File, Check, UserFollowing
from .serializers import UserSerializer, ChangePasswordSerializer, FileSerializers, CurrentUserSerializers, \
    ProfileSerializers
import pyrebase

# for signup

with open("/home/anant/PycharmProjects/API/Django/firebase.json", "r") as read_file:
    j = json.load(read_file)


firebase = pyrebase.initialize_app(j)
storage = firebase.storage()


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        obj = serializer.save()
        UserProfile.objects.create(user=obj)


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
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# image based work
class UserProfilePicture(APIView):
    permission_classes = ([IsAuthenticated])
    parser_classes = ([MultiPartParser])

    def put(self, request):
        print(request.data)
        if 'image' not in request.data:
            return Response(status=status.HTTP_204_NO_CONTENT)
        f = request.data['image']
        # USE models.ImageField IF YOU HAVE AWS, GCP or Azure, right now Iam using Firebase storage
        # so I will store file name as string in database and file in firebase storage

        # NOTE: Never use this Method in Production mode. It's highly insecure because we can access these files
        # in frontend without any authentication

        # I didn't find any proper documentation for Using Firebase storage with Django Media Files
        # that's why I am using this logic

        file_ext = str(request.data["image"]).split('.')[1]
        file_name = str(self.request.user.id) + "__" + \
                    str(datetime.datetime.now().isoformat()) + "." + file_ext
        storage.child("files/" + file_name).put(f)
        file1 = UserProfile.objects.get(user=request.user)
        print(file1)
        file1.avatar = f"files/{file_name}"
        file1.save()
        return Response(status=status.HTTP_201_CREATED)

    # def delete(self, request, pk):
    #     try:
    #         file = File.objects.get(user=request.user)
    #     except File.DoesNotExist:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     file.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def userDetails(request, pk):
    user = User.objects.get(id=pk)
    serial = CurrentUserSerializers(user)
    if serial:
        return Response(serial.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
def allUserDetails(request):
    user = User.objects.all()
    serial = CurrentUserSerializers(user, many=True)
    if serial:
        return Response(serial.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserDetail(APIView):
    permission_required = IsAuthenticated

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        serial = CurrentUserSerializers(user)
        return Response(serial.data, status=status.HTTP_200_OK)


#
@api_view(['POST', 'PUT'])
@permission_required([IsAuthenticated])
def followingfollow(request, pk):
    pkuser = User.objects.get(id=pk)
    UserFollowing.objects.create(follower_user_id=request.user,
                                 following_user_id=pkuser)
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
def other_followinglist(request, pk):
    s = User.objects.get(id=pk).following.all().values()
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


@api_view(["GET"])
def other_followerlist(request, pk):
    s = User.objects.get(id=pk).following.all().values()
    print(list(s))
    l = []
    for i in list(s):
        print(i["follower_id"])
        l.append(i["follower_id"])
    return JsonResponse({
        'followers': l
    })


def home(request):
    return render(request, "user/home.html")
