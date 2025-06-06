from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("create/<int:embassy_id>/", views.created_review, name="create"),  # POST로 후기 작성
    path("delete/<int:review_id>/", views.delete_review, name="delete"),    # POST로 후기 삭제
    path("helpful/<int:review_id>/", views.toggle_helpful, name="helpful"), # POST로 도움돼요 토글
    path("update/<int:review_id>/", views.update_review, name="update"),    # POST로 후기 수정
]