from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework.authentication import FirebaseAuthentication
from django.contrib.auth import login


class FirebaseLoginSignupView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        user = request.user

        # 이미 로그인된 경우
        if user.is_authenticated:
            return Response(
                {"message": "Already logged in."}, status=status.HTTP_200_OK
            )
        else:
            # Firebase UID를 기반으로 한 사용자 생성
            uid = request.auth.get("uid")
            user, created = User.objects.get_or_create(username=uid)

            # 사용자를 로그인 상태로 유지
            login(request, user)

            return Response(
                {"message": "Login successful."}, status=status.HTTP_200_OK
            )
