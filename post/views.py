from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView
from rest_framework import generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, PostComment
from .serializer import PostSerializers, CommentSerializer


class PostListView(ListView):
    model = Post
    context_object_name = 'post'
    ordering = ['-date_posted']


# https://naughty18.herokuapp.com/invite/5

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', "post_image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def detail_view(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = post.comments.all()
    return render(request, "post/post_detail.html", {'object': post, 'comments': comments})


@login_required
def like_disliked(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    print("Total", post.likes.count())
    url = reverse("post-detail", kwargs={"post_id": post.id})
    return HttpResponseRedirect(url)


@login_required
def addcomment(request, post_id):
    if request.method == "POST":
        comment = request.POST.get("comment")
        post = Post.objects.get(id=post_id)
        postcomment = PostComment(body=str(comment), post=post, user=request.user)
        postcomment.save()

    url = reverse("post-detail", kwargs={"post_id": post_id})
    return HttpResponseRedirect(url)


@login_required
def delete_comment(request, pk, c):
    comment = PostComment.objects.get(id=c)
    comment.delete()
    url = reverse("post-detail", kwargs={"post_id": pk})
    return HttpResponseRedirect(url)


@login_required
def search(request):
    if request.method == "POST":
        if request.POST.get("search"):
            data = request.POST.get("search")
            post = Post.objects.filter(title__icontains=data)
            user = User.objects.filter(username__icontains=data)
            context = {
                'post': post,
                'user_list': user,
            }
            return render(request, 'post/search.html', context)


class ArticleList(generics.ListCreateAPIView):
    queryset = PostComment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer


# operations with id
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializers


@api_view(['GET', 'POST'])
def comment(request, pk):
    if request.method == 'GET':
        postcomment = PostComment.objects.filter(post=pk)
        commentserial = CommentSerializer(postcomment, many=True)
        return Response(commentserial.data)
    elif request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT', 'DELETE'])
def comment_update(request, ci):
    try:
        comment = PostComment.objects.get(id=ci)
    except:
        return
    if request.method == "PUT":
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_required(IsAuthenticated)
@api_view(["GET", "POST"])
def like_dislike_api(request, pk):
    post = Post.objects.get(id=pk)
    if request.user.is_authenticated():
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)

