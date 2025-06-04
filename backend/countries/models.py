from django.db import models
from django.conf import settings

# 안전정보 api 모델 - [안전 공지]
class CountrySafety(models.Model):
    safety_id=models.CharField(max_length=30, unique=True) # id
    country_name = models.CharField(max_length=50)  # 한글 국가명
    country_en_name = models.CharField(max_length=50)  # 영문 국가명
    title = models.CharField(max_length=255)  # 제목
    content = models.TextField()  # 내용
    file_url = models.URLField(blank=True, null=True)  # 첨부파일 경로 (선택값)
    written_dt = models.DateField() # wrtDt (작성일)

    def __str__(self):
        return f"{self.country_name} - {self.title}"

# 안전공지 api 모델 - [유의지역 정보]
class SafetyNotice(models.Model):
    notice_id = models.CharField(max_length=30, unique=True)  # sfty_notice_id
    country_name = models.CharField(max_length=50)            # country_nm
    country_en_name = models.CharField(max_length=50)         # country_eng_nm
    title = models.CharField(max_length=255)                  # title
    content = models.TextField()                              # txt_origin_cn (HTML 포함됨)
    category = models.CharField(max_length=20)                # ctgy_nm ("안내", "주의" 등)
    written_dt = models.DateField()                           # wrt_dt
    file_url = models.URLField(blank=True, null=True)         # file_download_url (있을 수도 있음)

    def __str__(self):
        return f"{self.country_name} - {self.title}"