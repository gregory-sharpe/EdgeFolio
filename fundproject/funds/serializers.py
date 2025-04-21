# rest framework might be the way to go
# Using serializers was mentioned in the interview
from rest_framework import serializers
from .models import Fund


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = '__all__'
