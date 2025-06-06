from django.db import models
from django.conf import settings # 사용자 모델을 참조하기 위함
from countries.models import Embassy # 후기 대상이 되는 공관 모델

# 후기 모델
class Review(models.Model):
    # settings.AUTH_USER_MODEL : Django 설정에 등록된 사용자 모델
    # on_delete=models.CASCAD : 유저 삭제 시 해당 유저의 리뷰도 삭제됨
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    embassy = models.ForeignKey(Embassy, on_delete=models.CASCADE, related_name='reviews') # e.reviews로 해당 공관의 모든 리뷰 접근 가능
    content = models.TextField() # 후기 내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성 시 자동 저장
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시 자동 갱신

# 도움돼요 모델 (붐업)
class Helpfulness(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpfulness') # review.helpfulness로 접근 가능
    created_at = models.DateTimeField(auto_now_add=True) # 도움 누른 시점

    class Meta:
        unique_together = ('user', 'review') # 중복 방지