from django.urls import path

from countries import views

urlpatterns = [
    path("<slug:slug>/", views.keyword_warning_view, name='country_detail'),
    path("api/countries/", views.country_list_api, name='country_list_api'),
]