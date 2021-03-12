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
from .serializers import UserSerializer, ChangePasswordSerializer, FileSerializers, CurrentUserSerializers, ProfileSerializers


# for signup
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
    # permission_classes = ([IsAuthenticated])
    parser_classes = ([MultiPartParser])

    def put(self, request):
        print(request.data)
        if 'image' not in request.data:
            return Response(status=status.HTTP_204_NO_CONTENT)
        f = request.data['image']
        file1 = UserProfile.objects.get(user=request.user)
        print(file1)
        file1.avatar = f
        file1.save()
        return Response(status=status.HTTP_201_CREATED)

    # def post(self, request, pk):
    #     if 'file' not in request.data:
    #         raise Response(status=status.HTTP_204_NO_CONTENT)
    #     f = request.data['file']
    #     file1 = File(user=request.user, file=f)
    #     file1.save()
    #     return Response(status=status.HTTP_201_CREATED)

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


# curl -H "Authorization: Token b2eb41ed04493534120f4633078a2701b1fa4418"  http://127.0.0.1:8000/api/user/
# current user's post
# class UserPostList(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         try:
#             posts = self.request.user.posts
#         except:
#             Response({"error": "Data not found"}, status=status.HTTP_204_NO_CONTENT)
#
#         serial = PostSerializers(posts, many=True)
#         return Response(serial.data, status=status.HTTP_200_OK)


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
    #
    pkuser = User.objects.get(id=pk)
    # pkuser.follower.add(Follower.objects.create(follower=cpkuser))
    # cpkuser.following.add(Following.objects.create(following=pkuser))
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
