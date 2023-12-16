from rest_framework import generics, viewsets
from .models import Stock, League, Team, SeasonData, Venue, Player, News
from .serializers import (
    StockOverviewSerializer,
    TeamSerializer,
    LeagueSerializer,
    PlayerSerializer,
    VenueSerializer,
    NewsSerializer,
    SeasonDataSerializer,
)
from rest_framework.permissions import AllowAny

from rest_framework.response import Response


class StockOverviewList(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockOverviewSerializer
    permission_classes = [AllowAny]


class TeamInfoViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_class = [AllowAny]

    # All players related to the team
    # The venue of the team
    # Data of the league to which the team belongs
    def retrieve(self, request, *args, **kwargs):
        code = request.GET.get("code")
        team = Team.objects.get(code=code)
        league = team.league
        venue = Venue.objects.get(team=team)
        news = News.objects.filter(team=team).order_by("-published_date")[:12]
        season = SeasonData.objects.filter(league=league)
        team_data = TeamSerializer(team).data
        league_data = LeagueSerializer(league).data
        venue_data = VenueSerializer(venue).data
        news_data = NewsSerializer(news, many=True).data
        season_data = SeasonDataSerializer(season, many=True).data
        positions = [
            "Attacker",
            "Midfielder",
            "Defender",
            "Goalkeeper",
        ]
        player_data_by_position = {}
        for position in positions:
            players = Player.objects.filter(team=team, position=position)
            player_data = PlayerSerializer(players, many=True).data
            player_data_by_position[position] = player_data
        response_data = {
            "team": team_data,
            "league": league_data,
            "venue": venue_data,
            "news": news_data,
            "season": season_data,
            "player": player_data_by_position,
        }

        return Response(response_data)
