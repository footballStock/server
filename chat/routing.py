from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        "ws/chat/(?P<room_id>[-\w]+)/$",
        consumers.ChatConsumer.as_asgi(),
    ),
    # re_path(
    #     "ws/chatlist/(?P<user_id>[-\w]+)/$",
    #     consumers.ChatListConsumer.as_asgi(),
    # ),
]
