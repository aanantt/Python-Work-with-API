from django.urls import path
import user.views as user_views

urlpatterns = [
    path('user/<int:pk>/', user_views.userDetails, name="user"),
    path('user/password/', user_views.UpdatePassword().as_view(), name="update password"),
    path('user/', user_views.allUserDetails, name="alluser"),
    path('user/profile/image/', user_views.UserProfilePicture().as_view(), name='image'),
    path('signup/', user_views.UserCreateAPIView().as_view(), name='signup-api'),
    path('user/update/<int:pk>/', user_views.UserUpdateAPIView().as_view(), name='user-update-api'),
    path('current/user/', user_views.CurrentUserDetail().as_view(), name='api-user'),
    path('follow/<int:pk>/', user_views.followingfollow, name='following'),
    path('followinglist/', user_views.followinglist, name='followinglist'),
    path('followinglist/<int:pk>/', user_views.other_followinglist, name='other_followinglist'),
    path('followerlist/', user_views.followerlist, name='followerlist'),
    path('followerlist/<int:pk>/', user_views.other_followerlist, name='other_followerlist'),

]