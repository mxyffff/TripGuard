from django.urls import path
from . import views  # 같은 디렉토리의 views.py에서 함수들을 import
# 다른 앱들과 URL 이름이 겹치지 않도록 app_name을 지정
app_name = "countries"

urlpatterns = [
    # 국가 상세 정보를 JSON 형태로 응답하는 API
    # 예: /countries/api/detail/china/
    path("api/detail/<slug:slug>/", views.country_detail_api, name="country_detail_api"),

    # 전체 국가 목록 (이름 + slug)을 JSON 형태로 응답하는 API
    # 예: /countries/api/list/
    path("api/list/", views.country_list_api, name="country_list_api"),
]