from rest_framework import serializers
from .models import TravelAlert

class TravelAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelAlert
        fields = '__all__'
