from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User as u, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from post.models import Post
from rest_framework import generics, status, permissions
from rest_framework.decorators import parser_classes, api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile, File
from .serializers import UserSerializer, ChangePasswordSerializer, FileSerializers
from post.serializer import PostSerializers


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UpdatePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            update_session_auth_hash(request, self.object)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
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


class UserPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            posts = self.request.user.posts
        except:
            Response({"error": "Data not found"}, status=status.HTTP_204_NO_CONTENT)

        serial = PostSerializers(posts, many=True)
        return Response(serial.data, status=status.HTTP_200_OK)


def home(request):
    return HttpResponse("<h1>Work with APIs</h1><br><h3>in process</h3>")