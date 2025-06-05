from django.urls import path

from countries import views

urlpatterns = [
    path('<str:country_en_name>/', views.keyword_warning_view, name='country_detail')
]