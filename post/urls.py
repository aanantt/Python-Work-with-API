
from django.urls import path
import post.views as post_views

urlpatterns = [
    path('post/list/', post_views.PostList().as_view(), name='list-api'),
    path('post/rud/<int:pk>/', post_views.PostRUD().as_view(), name='api'),
    path('post/images/<int:pk>/', post_views.PostImageList().as_view(), name='api-post-image'),
    path('post/create/', post_views.PostCreate().as_view(), name='api'),
    path('post/user/<int:pk>/', post_views.userallpost, name='user-post-api'),
    path('post/currentuser/', post_views.currentuserallpost, name='currentuser-post-api'),
    path('comment/<int:id>/', post_views.Comments().as_view(), name='api-comment-get'),
    path('reply/<int:id>/', post_views.Reply().as_view(), name='api-reply-get'),
    path('post/like/<int:post_id>/', post_views.like_disliked, name="like-disliked"),

]
