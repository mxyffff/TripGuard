from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q # Django ORM에서 복잡한 조건 필터링을 위함
from countries.models import SafetyNotice, CountrySafety, Embassy, EmbassyHomepage
from datetime import datetime, timedelta
from django.db.models import Case, When, Value, IntegerField

def keyword_warning_view(request, slug):
    # 대소문자 상관없이 소문자로 변환
    slug = slug.lower()
    # slug 기준으로 해당 국가의 재외공관(기준 모델) 가져오기
    embassy = get_object_or_404(Embassy, slug=slug)
    country_en_name = embassy.country_en_name # 영문 국가명
    country_name = embassy.country_name # 한글 국가명

    # 해당 국가의 모든 공관 가져오기 + 대사관 우선 정렬
    embassies = Embassy.objects.filter(
        country_en_name__iexact=country_en_name
    ).annotate(
        sort_priority=Case(
            When(embassy_name__icontains="대사관", then=Value(0)),
            default=Value(1),
            output_field=IntegerField(),
        )
    ).order_by("sort_priority", "embassy_name")

    # 각 embassy에 대해 홈페이지 URL 속성 임시 부여
    # 각 Embassy 객체(e)에 대응되는 홈페이지 URL을 꺼내서, .homepage_url이라는 임시 속성으로 붙여주는 작업
    for e in embassies:
        homepage_obj = getattr(e, "homepage", None) # e.homepage 가져오는 것을 시도하되 없으면 None 리턴
        e.homepage_url = homepage_obj.url if homepage_obj else None

    # 현재 시점 기준 1년 이내 작성된 공지만 필터링
    one_year_ago = datetime.today() - timedelta(days=365)
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

    # 각 키워드에 해당하는 공지 필터링
    filtered_notices = {}
    for topic, keywords in topics.items(): # 딕셔너리 순회 (topic : key, kewords(키워드 리스트) : value)
        q = Q() # Q 객체 초기화
        for kw in keywords:
            q |= Q(content__icontains=kw) # 키워드별 누적(content: 필드, __icontains: 대소문자 구분X)
        filtered_notices[topic] = base_queryset.filter(q).order_by("-written_dt") # 최신순 정렬

    return render(request, "countries/countries_detail.html", {
        "embassies": embassies,
        "country_en_name": country_en_name,
        "country_name":country_name,
        "travel_notices": filtered_notices["travel"],
        "theft_notices": filtered_notices["theft"],
        "disaster_notices": filtered_notices["disaster"],
        "protest_notices": filtered_notices["protest"],
    })

def country_list_api(request):
    countries = Embassy.objects.values("country_name", "country_en_name", "slug").distinct()
    return JsonResponse(list(countries), safe=False)