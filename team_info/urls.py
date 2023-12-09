from django.urls import path
from .views import StockOverviewList, TeamInfoViewSet

urlpatterns = [
    path(
        "stock_overview/",
        StockOverviewList.as_view(),
        name="stock-overview-list",
    ),
    path(
        "teams/",
        TeamInfoViewSet.as_view(
            {
                "get": "retrieve",
            }
        ),
    ),
]
