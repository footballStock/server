from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .authentication import FirebaseAuthentication


class FirebaseLoginSignupView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request):
        try:
            user = request.user
            return Response(
                {"message": "Login successful"}, status=status.HTTP_200_OK
            )
        except:
            uid = request.auth.get("uid")
            user, created = User.objects.get_or_create(username=uid)
            return Response(
                {"message": "Login successful."}, status=status.HTTP_200_OK
            )
