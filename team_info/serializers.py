from rest_framework import serializers
from .models import Team, Stock


class StockOverviewSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(
        source="team.name", read_only=True
    )  # Team 모델의 name 필드와 연결

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
