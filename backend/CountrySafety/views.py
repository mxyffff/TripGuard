from rest_framework import viewsets
from .models import TravelAlert
from .serializers import TravelAlertSerializer

class TravelAlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TravelAlert.objects.all()
    serializer_class = TravelAlertSerializer
