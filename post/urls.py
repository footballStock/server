from django.urls import path
from . import views

urlpatterns = [
    path(
        "posts/",
        views.PostViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "posts/<int:pk>/",
        views.PostViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "posts/<int:pk>/like/",
        views.PostViewSet.as_view({"post": "like"}),
        name="post-like",
    ),
    path(
        "posts/<int:pk>/dislike/",
        views.PostViewSet.as_view({"post": "dislike"}),
        name="post-dislike",
    ),
    path(
        "posts/<int:post_pk>/comments/",
        views.CommentViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "comments/<int:pk>/",
        views.CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
]
