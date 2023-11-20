from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os, datetime


def random_name():
    unique_id = uuid.uuid4()
    name = str(unique_id).replace("-", "").lower()
    name = name[:6]

    return "User" + name


class User(AbstractUser):
    def profile_directory_path(instance, filename):
        file = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return f'profile/{instance.nickname}_profile_{datetime.datetime.now().strftime("%Y_%m_%dT%H%M")}{extension}'

    username = models.CharField(max_length=128, unique=True)
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
    profile = models.ImageField(
        upload_to=profile_directory_path,
        height_field=None,  # [TODO] Edit it
        width_field=None,
        blank=True,
        default="profile/default.png",
        verbose_name="프로필 사진",
    )

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name_plural = "User"
