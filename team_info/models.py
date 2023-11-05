from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=255)  # 팀 이름
    league = models.CharField(max_length=255)  # 소속 리그

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Teams"


class Stock(models.Model):
    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="stock_info", null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 주식 가격
    price_unit = models.CharField(max_length=20)  # 단위 필드 추가
    currency = models.CharField(max_length=10)  # 통화
    change = models.DecimalField(max_digits=10, decimal_places=2)  # 가격 변동
    change_percentage = models.DecimalField(
        max_digits=5, decimal_places=2
    )  # 가격 변동률
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)  # 시가 총액
    volume = models.IntegerField()  # 거래량

    def __str__(self):
        return self.team.name  # 팀 이름으로 주식 정보를 식별

    class Meta:
        verbose_name_plural = "Stocks"
