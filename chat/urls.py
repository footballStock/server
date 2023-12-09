from django.urls import path
from . import views

urlpatterns = [
    path(
        "chats/<int:room_pk>/",
        views.ChatViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        "chats/rooms/",
        views.ChatViewSet.as_view(
            {
                "get": "room_list",
            }
        ),
    ),
]