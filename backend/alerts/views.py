
# Create your views here.
from django.shortcuts import render
from .models import TravelAlert

def travel_alert_list(request):
    alerts = TravelAlert.objects.all()
    return render(request, 'alerts/list.html', {'alerts': alerts})
