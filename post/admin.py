from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)  # Post 모델 등록
admin.site.register(Comment)  # Comment 모델 등록
