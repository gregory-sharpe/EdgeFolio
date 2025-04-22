
from rest_framework import generics  # generic views and stuff
from .models import Fund
from .serializers import FundSerializer  # for object conversion
# Response but better for Django HTML
# for later
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from django.db.models import Q  # for complex queries
# from rest_framework import status

# List Funds (with optional filtering)

# using class based views as its a common design that has been done before


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
