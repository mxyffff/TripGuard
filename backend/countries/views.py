from django.http import JsonResponse, Http404  # JSON 응답을 위한 모듈
from django.shortcuts import get_object_or_404  # 객체를 가져오거나 404 에러 반환
from django.db.models import Q, Case, When, Value, IntegerField  # 복합 조건과 정렬을 위한 ORM 도구들
from countries.models import Embassy, EmbassyHomepage, CountrySafety, SafetyNotice  # 관련 모델들 import
from reviews.models import Review  # 리뷰 모델 import
from datetime import datetime, timedelta  # 날짜 계산을 위한 표준 모듈

def country_detail_api(request, slug):
    """
    [API] 특정 국가의 전체 상세 데이터를 JSON으로 제공하는 API입니다.
    - URL에서 받은 slug로 국가를 식별
    - 대사관 목록, 공지 키워드, 최신 공지, 후기 목록을 포함한 JSON 응답 반환
    """

    # slug는 국가를 식별하는 고유 문자열 (예: "china")
    # 소문자로 변환하여 대소문자 차이로 인한 오류 방지
    slug = slug.lower()

    # slug에 해당하는 모든 재외공관(Embassy)을 가져옴
    embassies = Embassy.objects.filter(slug=slug)

    # slug가 잘못된 경우
    if not embassies.exists():
        raise Http404("해당 국가의 공관 정보가 없습니다.")

    # 대표 공관 하나를 선택 (대사관이 있으면 그걸 우선)
    representative = (
            embassies.filter(embassy_name__icontains="대사관").first()
            or embassies.first()
    )

    # 이후 country_en_name과 country_name은 대표 공관 기준으로 가져옴
    country_en = representative.country_en_name
    country_ko = representative.country_name

    # 같은 국가의 다른 공관들을 모두 가져옴
    # '대사관'이 들어간 이름을 우선 정렬하기 위해 Case/When을 사용
    embassies = Embassy.objects.filter(
        country_en_name__iexact=country_en  # 영문 국가명이 같은 공관들 필터 (대소문자 구분 X)
    ).annotate( # 추가 필드
        sort_priority=Case(
            When(embassy_name__icontains="대사관", then=Value(0)),  # 대사관 우선
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by("sort_priority", "embassy_name")

    # 각 공관 데이터를 JSON 형태로 정리
    embassy_list = []
    for e in embassies:
        # 관련된 homepage가 있으면 가져오고, 없으면 None 처리
        homepage_url = e.homepage.url if hasattr(e, 'homepage') else None

        embassy_list.append({
            "id": e.id,
            "embassy_name": e.embassy_name,
            "address": e.address,
            "tel_no": e.tel_no,
            "urgency_tel": e.urgency_tel,
            "lat": e.lat,
            "lng": e.lng,
            "homepage_url": homepage_url,
        })

    # 최근 1년 이내의 유의 공지사항을 가져오기 위해 기준 날짜 계산
    one_year_ago = datetime.today() - timedelta(days=365)

    # 공지사항 필터링 (해당 국가 + 최근 1년 이내 작성된 것만)
    base_queryset = SafetyNotice.objects.filter(
        country_en_name__iexact=country_en,
        written_dt__gte=one_year_ago
    )

    # 카테고리별 키워드 정의 (이 키워드로 유의 공지를 분류)
    topic_keywords = {
        "여행": ["여행", "심사", "안전", "파업", "군사", "분쟁", "전쟁", "군대"],
        "범죄": ["소매치기", "절도", "치안", "범죄", "분실", "도난"],
        "자연재해": ["지진", "홍수", "태풍", "산불", "화산", "화재", "폭우", "폭설"],
        "시위": ["시위", "데모", "폭동"]
    }

    # 키워드별로 공지사항을 분류하고 title만 추출
    category_map = {}
    seen_titles = set()  # 중복 제거용
    for category, keywords in topic_keywords.items():
        q = Q()
        for kw in keywords:
            q |= Q(content__icontains=kw)  # 키워드가 포함된 공지를 모두 찾음
        matches = base_queryset.filter(q).order_by("-written_dt")
        titles = []
        for title in matches.values_list("title", flat=True): # 공지 중복 방지
            if title not in seen_titles:
                titles.append(title)
                seen_titles.add(title)
        if titles:
            category_map[category] = titles

    # 국가별 최신 공지사항 (CountrySafety 모델)
    safety_notices = CountrySafety.objects.filter(
        country_en_name__iexact=country_en
    ).order_by("-written_dt")

    # JSON 변환
    safety_data = [
        {
            "title": s.title,
            "content": s.content,
            "written_dt": s.written_dt.strftime("%Y-%m-%d"),
            "file_url": s.file_url
        }
        for s in safety_notices
    ]

    # 후기 리스트 조회 (현재 slug에 해당하는 대표 재외공관 기준)
    reviews = Review.objects.filter(embassy=representative).select_related('user').order_by('-created_at')

    # JSON 변환
    review_data = [
        {
            "id": r.id,
            "nickname": r.user.nickname,  # 사용자 닉네임
            "content": r.content,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M"),
            "helpfulness": r.helpfulness.count()
        }
        for r in reviews
    ]

    # 최종 JSON 응답 반환
    return JsonResponse({
        "country_name": country_ko,
        "country_en_name": country_en,
        "embassies": embassy_list,
        "category_map": category_map,
        "country_safeties": safety_data,
        "reviews": review_data
    }, json_dumps_params={'ensure_ascii': False})  # 한글 깨짐 방지 설정

def country_list_api(request):
    countries = Embassy.objects.values("country_name", "country_en_name", "slug").distinct()
    return JsonResponse(list(countries), safe=False)