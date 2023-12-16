from django.db import models
import os


class League(models.Model):
    name = models.CharField(max_length=255)  # League name
    country = models.CharField(max_length=255)  # Country of the league
    api_id = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Leagues"


class Team(models.Model):
    name = models.CharField(max_length=255)  # Team name
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
    league = models.ForeignKey("League", on_delete=models.CASCADE)
    team = models.CharField(max_length=255)
    season_year = models.IntegerField()
    matches_played = models.IntegerField()  # Matches Played
    wins = models.IntegerField()  # Wins
    draws = models.IntegerField()  # Draws
    loses = models.IntegerField()  # Losses
    goals_for = models.IntegerField()  # Goals For
    goals_against = models.IntegerField()  # Goals Against
    goal_difference = models.IntegerField()  # Goal Difference
    points = models.IntegerField()  # Points

    def __str__(self):
        return f"{self.team} - {self.season_year} Season"


class Stock(models.Model):
    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, related_name="stock_info"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Stock price
    price_unit = models.CharField(
        max_length=20, default="USD"
    )  # Unit field added
    currency = models.CharField(max_length=10)  # Currency
    change = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Price change
    change_percentage = models.DecimalField(
        max_digits=5, decimal_places=2
    )  # Price change percentage
    market_cap = models.DecimalField(
        max_digits=15, decimal_places=2
    )  # Market capitalization
    volume = models.IntegerField()  # Trading volume

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
        ("league", "League Match"),
        ("cup", "Cup Match"),
    )

    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="match_info"
    )
    venue = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="match_venue"
    )
    result = models.CharField(max_length=255)  # Match result
    opponent = models.CharField(max_length=255)  # Opponent
    match_type = models.CharField(
        max_length=10, choices=MATCH_TYPES
    )  # Type of match
    match_date = models.DateField()  # Match date

    def __str__(self):
        return f"{self.match_type} - {self.opponent}"

    class Meta:
        verbose_name_plural = "Matches"


class Player(models.Model):
    def player_directory_path(instance, filename):
        # Function to set the file path for player photos
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
    detailed_position = models.CharField(max_length=255, blank=True)
    api_id = models.SmallIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Players"


class News(models.Model):
    def news_directory_path(instance, filename):
        # Function to set the file path for news images
        file = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return f"news/{filename}"

    title = models.CharField(max_length=200)
    url = models.URLField()  # Field to store URL
    published_date = models.DateTimeField()  # Store the time of publication
    thumbnail = models.URLField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)

    def __str__(self):
        return f"[{self.team.name}] {self.title}"
