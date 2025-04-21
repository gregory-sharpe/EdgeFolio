
from rest_framework import generics  # generic views and stuff
from .models import Fund
from .serializers import FundSerializer  # for object conversion
# Response but better for Django HTML
from rest_framework.response import Response
# Decorators for API_views. Get, Post etc
from rest_framework.decorators import api_view
from django.db.models import Q  # for complex queries
# List Funds (with optional filtering)


class FundListAPIView(generics.ListAPIView):
    serializer_class = FundSerializer

    def get_queryset(self):
        queryset = Fund.objects.all()
        strategy = self.request.query_params.get('strategy')
        if strategy:
            queryset = queryset.filter(strategy__iexact=strategy)
        return queryset

# Retrieve single Fund by ID


class FundDetailAPIView(generics.RetrieveAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    lookup_field = 'id'
