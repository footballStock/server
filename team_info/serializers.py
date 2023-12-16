from rest_framework import serializers
from .models import Team, Stock, League, Player, Venue, News, SeasonData


class StockOverviewSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = Stock
        fields = (
            "team_name",
            "price",
            "price_unit",
            "currency",
            "change",
            "change_percentage",
            "market_cap",
            "volume",
        )


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = "__all__"


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class SeasonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonData
        fields = "__all__"
