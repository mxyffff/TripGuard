# serializers.py
from rest_framework import serializers
from .models import TravelWarning

class TravelWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelWarning
        fields = '__all__'
