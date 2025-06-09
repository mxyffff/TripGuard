from django.urls import path  # URL 경로 설정용 모듈
from . import views  # views.py에 정의된 함수들을 불러옴

# 앱 이름 설정 (config/urls.py에서 include(..., namespace="reviews") 사용 중이므로 필수)
app_name = "reviews"

urlpatterns = [
    # [1] 후기 작성 API
    # - POST 요청: /reviews/create/3/
    # - body: content=<내용>
    # - 3은 공관(Embassy)의 ID
    path("create/<slug:slug>/", views.create_review_api, name="create"),

    # [2] 후기 삭제 API
    # - POST 요청: /reviews/delete/5/
    # - 5는 삭제할 review의 ID
    path("delete/<int:review_id>/", views.delete_review_api, name="delete"),

    # [3] 후기 수정 API
    # - POST 요청: /reviews/update/5/
    # - body: content=<수정된 내용>
    # - 5는 수정할 review의 ID
    path("update/<int:review_id>/", views.update_review_api, name="update"),

    # [4] 도움돼요 토글 API
    # - POST 요청: /reviews/helpful/5/
    # - 5는 해당 review의 ID
    # - 자기 글엔 도움 안됨, 이미 눌렀으면 취소됨
    path("helpful/<int:review_id>/", views.toggle_helpful_api, name="helpful"),
]