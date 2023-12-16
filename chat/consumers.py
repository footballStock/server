from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import ChatRoom, Message
from accounts.models import User
import json
import datetime
import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


@database_sync_to_async
def get_room(room_id):
    # Retrieve a chat room by its ID asynchronously
    try:
        room = ChatRoom.objects.get(id=room_id)
        return room
    except ChatRoom.DoesNotExist:
        return None


def get_user(user_id):
    # Retrieve a user by their ID
    user = User.objects.get(id=user_id)
    return user


def save_message(room, user, message, timestamp):
    # Save a new message in the specified chat room
    user = User.objects.get(nickname=user["nickname"])
    new_message = Message(
        room_id=room, sender=user, content=message, timestamp=timestamp
    )
    new_message.save()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Establish a WebSocket connection
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Add the WebSocket to the channel layer group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Handle WebSocket disconnection
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        # Receive a message from WebSocket
        text_data_json = json.loads(text_data)
        content = text_data_json["content"]
        user = text_data_json["user"]
        timestamp = datetime.datetime.now()
        save_message(self.room_name, user, content, timestamp)

        # Send the message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": content,
                "user": user,
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"),
            },
        )

    def chat_message(self, event):
        # Send a message to WebSocket
        content = event["content"]
        user = event["user"]
        timestamp = event["timestamp"]

        self.send(
            text_data=json.dumps(
                {"content": content, "user": user, "timestamp": timestamp}
            )
        )
