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
from post import views as post_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from samplelogin import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home),
    path('api/image/', user_views.UserProfile().as_view(), name='image'),
    path('api/signup/', user_views.UserCreateAPIView().as_view(), name='signup-api'),
    path('api/user/<int:pk>/', user_views.UserUpdateAPIView().as_view(), name='user-api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/', post_views.ArticleList().as_view(), name='api'),
    path('api/current/', user_views.UserPost().as_view(), name='curr-post'),
    path('api/comment/<int:pk>/', post_views.comment, name='api-comment-get'),
    path('api/comment/update/<int:ci>/', post_views.comment_update, name='api-comment-get'),
    path('post/like/<int:post_id>/', post_views.like_disliked, name="like-disliked"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
