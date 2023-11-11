from django.urls import path
from . import views

urlpatterns = [
    # 포스트 목록 조회
    path(
        "posts/",
        views.PostViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    # 포스트 개별 조회, 수정, 삭제
    path(
        "posts/<int:pk>/",
        views.PostViewSet.as_view(
            {
                "get": "retrieve",
                "post": "create",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
    # 댓글 목록 조회
    path(
        "posts/<int:post_pk>/comments/",
        views.CommentViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    # 댓글 생성, 수정, 삭제
    path(
        "comments/<int:pk>/",
        views.CommentViewSet.as_view(
            {
                "get": "retrieve",
                "post": "create",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
]
