from django.http import Http404
from django.shortcuts import render
from django.db.models import Q # Django ORM에서 복잡한 조건 필터링을 위함
from countries.models import SafetyNotice, CountrySafety
from datetime import datetime, timedelta

def keyword_warning_view(request, country_en_name):
    # 국가 존재 여부 먼저 확인
    if not SafetyNotice.objects.filter(country_en_name__iexact=country_en_name).exists():
        raise Http404("존재하지 않는 국가입니다.")

    # 현재 시점 기준 1년 이내로 제한 기준 생성
    one_year_ago = datetime.today() - timedelta(days=365)
    # 1년 이내 기준으로 필터링
    base_queryset = SafetyNotice.objects.filter(
        country_en_name__iexact=country_en_name,
        written_dt__gte=one_year_ago
    )

    # 주제별 키워드 정의 - 딕셔너리
    topics = {
        "travel": ["여행", "심사", "안전", "파업"], # 여행 주의 키워드
        "theft": ["소매치기", "절도", "치안", "범죄", "분실", "도난"], # 소매치기, 절도 관련 키워드
        "disaster": ["지진", "홍수", "산불", "화산", "화재", "폭우", "폭설"], # 자연재해 키워드
        "protest": ["시위", "데모", "폭동"], # 시위 키워드
    }

    # 각 키워드에 해당하는 공지 추출
    filtered_notices = {}
    for topic, keywords in topics.items(): # 딕셔너리 순회 (topic : key, kewords(키워드 리스트) : value)
        q = Q() # Q 객체 초기화
        for kw in keywords:
            q |= Q(content__icontains=kw) # 키워드별 누적(content: 필드, __icontains: 대소문자 구분X)
        filtered_notices[topic] = base_queryset.filter(q).order_by("-written_dt") # 최신순 정렬

    return render(request, "countries/countries_detail.html", {
        "travel_notices": filtered_notices["travel"],
        "theft_notices": filtered_notices["theft"],
        "disaster_notices": filtered_notices["disaster"],
        "protest_notices": filtered_notices["protest"],
    })