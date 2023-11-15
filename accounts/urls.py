from django.urls import path
from . import views

urlpatterns = [
    # 포스트 목록 조회
    path(
        "login/",
        views.FirebaseLoginSignupView.as_view(
            {
                "post": "post",
            }
        ),
    ),
]
