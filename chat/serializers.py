from rest_framework import serializers
from .models import Message, ChatRoom

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        if obj.sender:
            user = obj.sender
            profile_data = {
                "src": user.profile.url if user.profile else "",
                "alt": user.nickname if user.nickname else "",
            }

            response_data = {
                "profile": profile_data,
                "nickname": user.nickname if user.nickname else "",
            }
            return response_data
        else:
            return None
    
    class Meta:
        model = Message
        fields = (
            "id",
            "content",
            "room",
            "user",
            "timestamp",
        )

class ChatRoomSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    def get_team(self, obj):
        return obj.team.name

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "team",
        )