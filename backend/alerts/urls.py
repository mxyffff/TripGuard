from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('alert_geojson/', views.alert_geojson, name='alert_geojson'),  # /api/alert_geojson/ 와 연결
    re_path(r'^(?P<country_code>[A-Za-z]{2,3})/$', views.alert_detail, name='alert_detail'),
]
