"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from post import views as post_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home),
    path('api/login/',obtain_auth_token,name = 'login'),
    path('api/user/<int:pk>/', user_views.userDetails, name="user"),
    path('api/user/password/', user_views.UpdatePassword().as_view(), name="update password"),
    path('api/user/', user_views.allUserDetails, name="alluser"),
    path('api/user/profile/image/', user_views.UserProfilePicture().as_view(), name='image'),
    path('api/user/signup/', user_views.UserCreateAPIView().as_view(), name='signup-api'),
    path('api/user/update/<int:pk>/', user_views.UserUpdateAPIView().as_view(), name='user-update-api'),
    path('api/post/list/', post_views.PostList().as_view(), name='list-api'),
    path('api/current/user/', user_views.CurrentUserDetail().as_view(), name='api-user'),
    path('api/post/rud/<int:pk>/', post_views.PostRUD().as_view(), name='api'),
    path('api/post/images/<int:pk>/', post_views.PostImageList().as_view(), name='api-post-image'),
    path('api/post/create/', post_views.PostCreate().as_view(), name='api'),
    path('api/post/user/<int:pk>/', post_views.userallpost, name='user-post-api'),
    path('api/post/currentuser/', post_views.currentuserallpost, name='currentuser-post-api'),
    # path('api/current/user/posts', user_views.UserPostList().as_view(), name='current-user-post'),
    path('api/follow/<int:pk>/', user_views.followingfollow, name='following'),
    path('api/followinglist/', user_views.followinglist, name='followinglist'),
    path('api/followinglist/<int:pk>/', user_views.other_followinglist, name='other_followinglist'),
    path('api/followerlist/', user_views.followerlist, name='followerlist'),
    path('api/followerlist/<int:pk>/', user_views.other_followerlist, name='other_followerlist'),
    path('api/comment/<int:id>/', post_views.Comments().as_view(), name='api-comment-get'),
    path('api/post/like/<int:post_id>/', post_views.like_disliked, name="like-disliked"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
