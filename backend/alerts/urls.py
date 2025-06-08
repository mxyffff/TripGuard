from django.urls import path
from . import views

urlpatterns = [
    path('geojson/', views.alert_geojson, name='alert_geojson'),
    path('<str:country_code>/', views.alert_detail, name='alert_detail'),
]
