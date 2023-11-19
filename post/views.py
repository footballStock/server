from rest_framework import generics, viewsets, status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.exceptions import PermissionDenied

from accounts.models import User

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response


# Post 목록 조회와 생성 API
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # 전체 Post 목록 조회
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 특정 Post 정보 가져오기
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # 새로운 Post 등록
    def create(self, request, *args, **kwargs):
        print(request.user.id)
        new_post = Post.objects.create(
            author=request.user,
            title=request.data["title"],
            content=request.data["content"],
        )
        new_post.save()
        serializer = PostSerializer(new_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 기존의 Post 수정
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        if instance.author != self.request.user:
            raise PermissionDenied(
                "You do not have permission to update this post."
            )
        serializer.save()
        return Response(serializer.data)

    # 기존의 Post 삭제
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied(
                "You do not have permission to update this post."
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Comment 목록 조회와 생성 API


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "update": [IsAuthenticated],
        "destroy": [IsAuthenticated],
        "list": [AllowAny],  # 인증이 필요하지 않은 권한으로 설정
        "retrieve": [AllowAny],  # 인증이 필요하지 않은 권한으로 설정
    }

    # 특정 Post에 달린 댓글 목록 조회
    def list(self, request, *args, **kwargs):
        # 특정 Post에 대한 댓글 목록만 조회
        post_id = self.kwargs.get("post_pk")
        queryset = self.queryset.filter(post_id=post_id)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    # 특정 댓글 정보 가져오기
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # 새로운 댓글 등록
    def create(self, request, *args, **kwargs):
        # 새로운 댓글을 게시하는 사용자를 현재 요청한 사용자로 설정
        request.data["user"] = request.user.id
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 기존의 댓글 수정
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CommentSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # 댓글을 등록한 사용자와 현재 요청한 사용자를 비교
        if instance.user != request.user:
            raise PermissionDenied(
                "You do not have permission to update this comment."
            )

        serializer.save()
        return Response(serializer.data)

    # 기존의 댓글 삭제
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # 댓글을 등록한 사용자와 현재 요청한 사용자를 비교
        if instance.user != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this comment."
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
