"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users.views import home_api_view

urlpatterns = [
    path("", home_api_view, name="home"),
    path('admin/', admin.site.urls),
    path('countries/', include('countries.urls')),
    path('auth/', include('users.urls', namespace="users")),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path('alerts/', include('alerts.urls')), # ← alerts_returnjson에서 가져온 부분
    path('api/', include('alerts.urls')),
    path("nation/", nation_page_view, name="nation_page_view"), # 추가
]   + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
