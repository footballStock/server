from django.urls import path
from .views import StockOverviewList

urlpatterns = [
    path(
        "stock_overview/",
        StockOverviewList.as_view(),
        name="stock-overview-list",
    ),
    # 다른 URL 패턴들을 여기에 추가할 수 있습니다.
]