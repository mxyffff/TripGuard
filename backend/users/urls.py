from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.login_api_view, name="login"),
    path("logout/", views.logout_api_view, name="logout"),
    path("signup/", views.signup_api_view, name="signup"),
]