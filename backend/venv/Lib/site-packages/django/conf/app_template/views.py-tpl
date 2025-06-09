from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q # Django ORM에서 복잡한 조건 필터링을 위함
from countries.models import SafetyNotice, CountrySafety, Embassy, EmbassyHomepage
from datetime import datetime, timedelta
from django.db.models import Case, When, Value, IntegerField

from reviews.models import Review


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

    # 대표 키워드별 하위 키워드 매핑
    topic_keywords = {
        "여행": ["여행", "심사", "안전", "파업", "군사", "분쟁", "전쟁", "군대"],
        "범죄": ["소매치기", "절도", "치안", "범죄", "분실", "도난"],
        "자연재해": ["지진", "홍수", "태풍", "산불", "화산", "화재", "폭우", "폭설"],
        "시위": ["시위", "데모", "폭동"]
    }

    category_map = {} # 최종 결과를 담을 딕셔너리
    seen_titles = set() # 중복 제거용: 이미 출력한 title을 기억
    for category, keywords in topic_keywords.items(): # 대표 키워드(category)별로 반복
        q = Q() # 각 카테고리마다 내부 키워드들에 대해 Q 객체를 생성
        for kw in keywords:
            q |= Q(content__icontains=kw) # content에 각 키워드가 포함된 공지를 모두 찾음 (OR 조건)
        # 키워드가 포함된 필터링된 공지를 가져오고, 최신순 정렬
        matches = base_queryset.filter(q).order_by("-written_dt")
        # 이 category에 속한 title들을 저장할 리스트
        titles = []
        for title in matches.values_list("title", flat=True): # 공지들의 title만 가져옴
            if title not in seen_titles: # 아직 출력한 적 없는 title만
                titles.append(title)
                seen_titles.add(title) # 중복 방지용으로 저장
        if titles:
            category_map[category] = titles # 결과 저장 (여행: [...], 범죄: [...], ...)

    # CountrySafety 공지 (우측 하단 출력용) 최신순
    country_safeties = CountrySafety.objects.filter(
        country_en_name__iexact=country_en_name
    ).order_by("-written_dt")

    # 댓글 조회
    # 최신순 + user FK join
    reviews = Review.objects.filter(embassy=embassy).select_related('user').order_by('-created_at')

    return render(request, "countries/countries_detail.html", {
        "embassies": embassies,
        "embassy": embassy, # 후기 등록 시 필요
        "country_en_name": country_en_name,
        "country_name": country_name,
        "category_map": category_map,
        "country_safeties": country_safeties,
        "reviews": reviews, # 후기 목록 템플릿 전달
    })


def country_list_api(request):
    countries = Embassy.objects.values("country_name", "country_en_name", "slug").distinct()
    return JsonResponse(list(countries), safe=False)