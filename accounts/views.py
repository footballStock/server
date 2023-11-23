from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .authentication import FirebaseAuthentication


class FirebaseLoginSignupView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        uid = request.auth.get("uid")
        user, created = User.objects.get_or_create(username=uid)
        profile_data = {
            "src": user.profile.url if user.profile else "",
            "alt": user.nickname if user.nickname else "",
        }

        response_data = {
            "profile": profile_data,
            "nickname": user.nickname if user.nickname else "",
        }

        return Response(response_data, status=status.HTTP_200_OK)
