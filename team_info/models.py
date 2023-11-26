from django.db import models
import os


class League(models.Model):
    name = models.CharField(max_length=255)  # 리그 이름
    country = models.CharField(max_length=255)  # 소속 국가
    api_id = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Leagues"


class Team(models.Model):
    name = models.CharField(max_length=255)  # 팀 이름
    team = models.OneToOneField(
        League, on_delete=models.CASCADE, related_name="player_info"
    )
    code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    founded = models.IntegerField()
    national = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Teams"


class Stock(models.Model):
    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="stock_info"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 주식 가격
    price_unit = models.CharField(max_length=20, default="USD")  # 단위 필드 추가
    currency = models.CharField(max_length=10)  # 통화
    change = models.DecimalField(max_digits=10, decimal_places=2)  # 가격 변동
    change_percentage = models.DecimalField(
        max_digits=5, decimal_places=2
    )  # 가격 변동률
    market_cap = models.DecimalField(max_digits=15, decimal_places=2)  # 시가 총액
    volume = models.IntegerField()  # 거래량

    def __str__(self):
        return self.team.name

    class Meta:
        verbose_name_plural = "Stocks"


class Venue(models.Model):
    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="venue_info"
    )
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    surface = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Venues"


class Match(models.Model):
    MATCH_TYPES = (
        ("league", "리그 경기"),
        ("cup", "컵 경기"),
    )

    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="match_info"
    )
    venue = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="match_venue"
    )
    result = models.CharField(max_length=255)  # 경기 결과
    opponent = models.CharField(max_length=255)  # 상대방
    match_type = models.CharField(max_length=10, choices=MATCH_TYPES)  # 경기 종류
    match_date = models.DateField()  # 경기 일정

    def __str__(self):
        return f"{self.match_type} - {self.opponent}"

    class Meta:
        verbose_name_plural = "Matches"


class Player(models.Model):
    def player_directory_path(instance, filename):
        file = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return f"profile/{instance.name}{extension}"

    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="player_info"
    )
    photo = models.ImageField(upload_to=player_directory_path)
    name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    detailed_position = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Players"
