from django.contrib import admin
from .models import CountrySafety

@admin.register(CountrySafety)
class CountrySafetyAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_en_name', 'title', 'written_dt') # 관리자 리스트에 보여줄 필드
    search_fields = ('country_name', 'country_en_name', 'title') # 검색창에서 검색 가능한 필드
    list_filter = ('written_dt',) # 오른쪽에 필터링 옵션 생성
