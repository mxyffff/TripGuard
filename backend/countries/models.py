from django.db import models
from django.conf import settings
from django.utils.text import slugify

# 안전정보 api 모델 - [안전 공지]
class CountrySafety(models.Model):
    safety_id=models.CharField(max_length=30, unique=True) # id
    country_name = models.CharField(max_length=50)  # 한글 국가명
    country_en_name = models.CharField(max_length=50)  # 영문 국가명
    title = models.CharField(max_length=255)  # 제목
    content = models.TextField()  # 내용
    file_url = models.URLField(blank=True, null=True)  # 첨부파일 경로 (선택값)
    written_dt = models.DateField() # wrtDt (작성일)

    def save(self, *args, **kwargs):
        # 기존 객체가 존재하면 country_name/en_name은 덮어쓰지 않음
        if self.pk:
            original = CountrySafety.objects.filter(pk=self.pk).first()
            if original:
                self.country_name = original.country_name
                self.country_en_name = original.country_en_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.country_name} - {self.title}"

# 안전 공지 api 모델 - [유의 지역 정보]
class SafetyNotice(models.Model):
    notice_id = models.CharField(max_length=30, unique=True)  # sfty_notice_id
    country_name = models.CharField(max_length=50)            # country_nm
    country_en_name = models.CharField(max_length=50)         # country_eng_nm
    title = models.CharField(max_length=255)                  # title
    content = models.TextField()                              # txt_origin_cn (HTML 포함됨)
    category = models.CharField(max_length=20)                # ctgy_nm ("안내", "주의" 등)
    written_dt = models.DateField()                           # wrt_dt
    file_url = models.URLField(blank=True, null=True)         # file_download_url (있을 수도 있음)

    def save(self, *args, **kwargs):
        # 기존 객체가 존재하면 country_name/en_name은 덮어쓰지 않음
        if self.pk:
            original = SafetyNotice.objects.filter(pk=self.pk).first()
            if original:
                self.country_name = original.country_name
                self.country_en_name = original.country_en_name
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.country_name} - {self.title}"

# 재외공관 정보 api - [재외공관 목록]
class Embassy(models.Model):
    embassy_cd = models.CharField(max_length=20, unique=True, default="temp_cd")  # 공관 코드 (PK 대용)
    country_name = models.CharField(max_length=50)  # 국가명 (한글)
    country_en_name = models.CharField(max_length=50)  # 국가명 (영문)

    # slug 추가 (path 경로명 전용 필드. 국가 단위로 구분)
    slug = models.SlugField(max_length=100, blank=True, null=True)  # 국가 단위 slug (공관마다 중복 허용!)

    embassy_name = models.CharField(max_length=100)  # 대사관명
    address = models.TextField()  # 대사관 주소
    tel_no = models.CharField(max_length=50, blank=True, null=True)  # 일반 전화번호
    urgency_tel = models.CharField(max_length=50, unique=True, blank=True, null=True)  # 긴급 연락처
    lat = models.FloatField(blank=True, null=True)  # 위도
    lng = models.FloatField(blank=True, null=True)  # 경도

    def save(self, *args, **kwargs):
        # country_name, country_en_name은 수동 보호!
        if self.pk:
            original = Embassy.objects.filter(pk=self.pk).first()
            if original:
                self.country_name = original.country_name
                self.country_en_name = original.country_en_name

        # 슬러그는 국가 기준으로 하나만 생성되게 처리
        if not self.slug:
            # 같은 국가명을 가진 공관 중 slug가 이미 있는 게 있으면 그걸 공유
            existing = Embassy.objects.filter(country_en_name__iexact=self.country_en_name, slug__isnull=False).exclude(
                pk=self.pk).first()
            if existing:
                self.slug = existing.slug
            else:
                # 없으면 새로 생성
                self.slug = slugify(self.country_en_name or self.country_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.country_name} - {self.embassy_name}"

# 재외공관 홈페이지 api
class EmbassyHomepage(models.Model):
    # Embassy 모델과 1:1 연결 관계
    embassy = models.OneToOneField("Embassy", on_delete=models.CASCADE, related_name="homepage")
    url = models.URLField()  # 홈페이지 URL

    def __str__(self):
        return f"{self.embassy.embassy_name} 홈페이지"