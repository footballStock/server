from rest_framework import generics, viewsets, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    BasePermission,
)
from rest_framework.exceptions import PermissionDenied

from accounts.models import User

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user and request.user.is_authenticated


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated],
        "destroy": [IsAuthenticated],
        "list": [AllowAny],
        "retrieve": [AllowAny],
        "like": [IsAuthenticated],
        "dislike": [IsAuthenticated],
    }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by("-created_at")
        page = request.GET.get("page")

        paginator = Paginator(queryset, 10)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_obj = paginator.page(page)

        serializer = self.get_serializer(page_obj, many=True)
        response_data = {
            "num_pages": paginator.num_pages,
            "posts": serializer.data,
        }
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user in instance.likes.all():
            like = True
        else:
            like = False
        if user in instance.dislikes.all():
            dislike = True
        else:
            dislike = False
        serializer_data = self.get_serializer(
            instance,
        ).data
        serializer_data["like"] = like
        serializer_data["dislike"] = dislike
        return Response(serializer_data)

    def top3post(self, request, *args, **kwargs):
        queryset = Post.objects.annotate(likes_count=Count("likes")).order_by(
            "-likes_count"
        )[:3]
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        new_post = Post.objects.create(
            author=request.user,
            title=request.data["title"],
            content=request.data["content"],
            image=request.FILES["image"],
        )
        new_post.save()
        serializer_data = serializer_data = self.get_serializer(
            new_post,
        ).data
        return Response(serializer_data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied(
                "You do not have permission to update this post."
            )
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.image = request.FILES["image"]
        post.save()
        serializer_data = self.get_serializer(
            post,
        ).data
        return Response(serializer_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied(
                "You do not have permission to update this post."
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            like = False
            dislike = False
        else:
            post.likes.add(user)
            post.dislikes.remove(user)
            like = True
            dislike = False

        serializer_data = self.get_serializer(
            post,
        ).data
        serializer_data["like"] = like
        serializer_data["dislike"] = dislike
        return Response(serializer_data)

    def dislike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.dislikes.all():
            post.dislikes.remove(user)
            like = False
            dislike = False
        else:
            post.dislikes.add(user)
            post.likes.remove(user)
            like = False
            dislike = True

        serializer_data = self.get_serializer(
            post,
        ).data
        serializer_data["like"] = like
        serializer_data["dislike"] = dislike
        return Response(serializer_data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated],
        "destroy": [IsAuthenticated],
        "list": [AllowAny],
        "retrieve": [AllowAny],
    }

    def list(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_pk")
        queryset = self.queryset.filter(post_id=post_id).order_by("-created_at")
        page = request.GET.get("page")

        paginator = Paginator(queryset, 10)

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_obj = paginator.page(page)

        serializer = self.get_serializer(page_obj, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if instance.user != request.user:
            raise PermissionDenied(
                "You do not have permission to update this comment."
            )

        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this comment."
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
