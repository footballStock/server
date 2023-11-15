from rest_framework import generics
from .models import Stock
from .serializers import StockOverviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class StockOverviewList(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockOverviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
