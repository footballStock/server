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
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name="player_info"
    )
    code = models.CharField(max_length=255)
    founded = models.IntegerField()
    national = models.BooleanField()
    api_id = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Teams"

class SeasonData(models.Model):
    league = models.ForeignKey('League', on_delete=models.CASCADE)
    team = models.CharField(max_length=255)
    season_year = models.IntegerField()
    matches_played = models.IntegerField()  # MP
    wins = models.IntegerField()  # W
    draws = models.IntegerField()  # D
    loses = models.IntegerField()  # L
    goals_for = models.IntegerField()  # G
    goals_against = models.IntegerField()  # Goals Against
    goal_difference = models.IntegerField()  # +/-
    points = models.IntegerField()  # P

    def __str__(self):
        return f"{self.team} - {self.season_year} Season"


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

    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="match_info"
    )
    venue = models.ForeignKey(
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
        return f"player/{instance.name}{extension}"

    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="player_info"
    )
    photo = models.ImageField(upload_to=player_directory_path, blank=True)
    name = models.CharField(max_length=255)
    number = models.SmallIntegerField(null=True)
    nationality = models.CharField(max_length=255, blank=True)
    position = models.CharField(max_length=255)
    detailed_position = models.CharField(max_length=255,  blank=True)
    api_id = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Players"

class News(models.Model):
    def news_directory_path(instance, filename):
        file = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return f"news/{filename}"
    title = models.CharField(max_length=200)
    url = models.URLField()  # URL을 저장하는 필드
    published_date = models.DateTimeField()  # 발행 시간을 직접 저장
    thumbnail = models.URLField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)

    def __str__(self):
        return f"[{self.team.name}] {self.title}"