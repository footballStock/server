from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


def random_name():
    unique_id = uuid.uuid4()
    name = str(unique_id).replace("-", "").lower()
    name = name[:6]

    return "User" + name


class User(AbstractUser):
    firebase_uid = models.CharField(max_length=128, blank=True, null=True)
    nickname = models.CharField(
        max_length=50,
        default=random_name,
        unique=True,
        verbose_name="닉네임",
    )
    name = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="이름",
    )

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = "User"
