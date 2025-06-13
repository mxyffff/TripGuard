from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_api_view, name="logout"),
    path("signup/", views.signup_page_view, name="signup"),
    path('signup/complete/', views.signup_complete_page_view, name='signup_complete'),

    path('api/login/', views.login_api_view),
    path('api/logout/', views.logout_api_view),
    path('api/signup/', views.signup_api_view),
]