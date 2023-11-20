from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async

from asgiref.sync import async_to_sync

from .models import ChatRoom, Message

from accounts.models import User
import json
import datetime
from django.db.models import Q
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@database_sync_to_async
def get_room(room_id):
    try:
        room = ChatRoom.objects.get(id=room_id)
        return room
    except ChatRoom.DoesNotExist:
        return None


@database_sync_to_async
def get_user(user_id):
    user = User.objects.get(id=user_id)
    return user


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = text_data_json["user"]
        timestamp = datetime.datetime.now()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user,
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            },
        )

    def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        timestamp = event["timestamp"]

        self.send(
            text_data=json.dumps(
                {"message": message, "user": user, "timestamp": timestamp}
            )
        )


# class ChatListConsumer(WebsocketConsumer):
#     async def connect(self):
#         self.user_id = int(self.scope["url_route"]["kwargs"]["user_id"])
#         self.user_group_name = f"user_{self.user_id}"
#         await self.channel_layer.group_add(
#             self.user_group_name, self.channel_name
#         )
#         await self.accept()
#         chatlist = await chat_list(self.user_id)
#         await self.send(text_data=json.dumps(chatlist))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.user_group_name, self.channel_name
#         )

#     async def receive_json(self, data):
#         data["type"] = "send_to_websocket"
#         await self.channel_layer.group_send(self.user_group_name, data)

#     async def send_to_websocket(self, event):
#         chatlist = await chat_list(self.user_id)
#         await self.send(text_data=json.dumps(chatlist))
