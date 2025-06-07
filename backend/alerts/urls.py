from django.urls import path, include
from .views import travel_alert_list
from rest_framework.routers import DefaultRouter
from .api_views import TravelAlertViewSet

router = DefaultRouter()
router.register(r'api/alerts', TravelAlertViewSet)

urlpatterns = [
    path('', travel_alert_list, name='travel_alert_list'),
    path('', include(router.urls)),
]
