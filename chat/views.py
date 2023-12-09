from rest_framework import generics, viewsets, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    BasePermission,
)
from rest_framework.exceptions import PermissionDenied

from accounts.models import User

from .models import Message, ChatRoom
from .serializers import MessageSerializer, ChatRoomSerializer
from rest_framework.response import Response
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes_by_action = {
        "list": [IsAuthenticated],
    }

    def list(self, request, *args, **kwargs):
        room_id = self.kwargs.get("room_pk")
        last_message_id = request.GET.get("last")  # 쿼리 파라미터로 'last_message_id'를 받음

        if last_message_id:
            message_ids = Message.objects.filter(room_id=room_id, id__lt=last_message_id).values_list('id', flat=True).order_by("-timestamp")[:10]
        else:
            message_ids = Message.objects.filter(room_id=room_id).values_list('id', flat=True).order_by("-timestamp")[:10]

        queryset = Message.objects.filter(id__in=message_ids).order_by("timestamp")

        serializer = self.get_serializer(queryset, many=True)


        return Response(serializer.data)
    
    def room_list(self, request, *args, **kwargs):
        queryset = ChatRoom.objects.all()
        serializer = ChatRoomSerializer(queryset, many=True)

        return Response(serializer.data)