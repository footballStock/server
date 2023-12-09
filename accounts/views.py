from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .authentication import FirebaseAuthentication


class FirebaseLoginSignupView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = [FirebaseAuthentication]

    def login(self, request, *args, **kwargs):
        # uid = request.auth.get("uid")
        # user, created = User.objects.get_or_create(username=uid)
        user = request.user
        profile_data = {
            "src": user.profile.url if user.profile else "",
            "alt": user.nickname if user.nickname else "",
        }

        response_data = {
            "profile": profile_data,
            "nickname": user.nickname if user.nickname else "",
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        user = request.user
        if "image" in request.FILES:
            user.profile = request.FILES["image"]
        if "nickname" in request.data:
            nickname = request.data["nickname"]
            if User.objects.filter(nickname=nickname).exclude(id=user.id).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                user.nickname = request.data["nickname"]
        user.save()

        profile_data = {
            "src": user.profile.url if user.profile else "",
            "alt": user.nickname if user.nickname else "",
        }

        response_data = {
            "profile": profile_data,
            "nickname": user.nickname if user.nickname else "",
        }

        return Response(response_data, status=status.HTTP_200_OK)
