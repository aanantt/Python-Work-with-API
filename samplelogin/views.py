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


def userr(request):
    user = User.objects.get(id=request.user.id)
    profile = UserProfile.objects.get(user=user)
    post = Post.objects.filter(author=request.user)
    context = {
        'user': user,
        'profile': profile,
        'post': post,
    }
    return render(request, 'samplelogin/userpage.html', context)


def register(request):
    if request.method == 'POST':
        forms = UserRegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            user1 = User.objects.get(username=forms.cleaned_data['username'])
            data = UserProfile(user=user1)
            data.save()
            return redirect('home')
        else:
            return HttpResponse("<h1>ERROR</h1>")
    if request.method == 'GET':
        form = UserRegistrationForm()
    return render(request, 'samplelogin/signup.html', {'form': form})


def userhome(request, user_id):
    user1 = u.objects.get(id=user_id)
    current_user = request.user
    post = Post.objects.filter(author=user1)
    profile = UserProfile.objects.filter(user=current_user)
    context = {
        "user": user1,
        "post": post,
        "profile": profile
    }
    return render(request, 'samplelogin/userpage.html', context)


def image(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print("valid")
            data = UserProfile(user=request.user, avatar=form.cleaned_data["avatar"])
            data.save()
            return redirect("home")
    elif request.method == "GET":
        form = UserProfileForm()
    return render(request, "samplelogin/image.html", {'form': form})


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


#
# @api_view(["PUT", "POST", "DELETE", "GET"])
# @parser_classes([MultiPartParser])
# @permission_classes([IsAuthenticated])
# def ProfileDP(request, format=None):
#     if request.method == "PUT":
#         if 'file' not in request.data:
#             raise Response(status=status.HTTP_204_NO_CONTENT)
#         f = request.data['file']
#         file1 = File.objects.get(user=request.user)
#         file1.file = f
#         file1.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method == "POST":
#         if 'file' not in request.data:
#             raise Response(status=status.HTTP_204_NO_CONTENT)
#         f = request.data['file']
#         file1 = File(user=request.user, file=f)
#         file1.save()
#         return Response(status=status.HTTP_201_CREATED)
#     elif request.method == "DELETE":
#         file = File.objects.get(user=request.user)
#         file.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == "GET":
#         file = File.objects.get(user=request.user)
#         serial = FileSerializers(file)
#         return Response(serial.data, status=status.HTTP_200_OK)


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
