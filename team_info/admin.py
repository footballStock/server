from django.contrib import admin
from .models import Stock, Team

admin.site.register(Stock)  # Stock 모델 등록
admin.site.register(Team)  # Team 모델 등록
