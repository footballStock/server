from rest_framework import generics
from .models import Stock
from .serializers import StockOverviewSerializer


class StockOverviewList(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockOverviewSerializer
