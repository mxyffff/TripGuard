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

    # 대표 공관: '대사관'이 들어간 이름이 우선, 없으면 첫 번째 공관
    representative = (
            embassies.filter(embassy_name__icontains="대사관").first()
            or embassies.first()
    )

    # 대표 공관 기준 국가명 추출
    country_en = representative.country_en_name
    country_ko = representative.country_name

    # 동일 국가의 공관 전체 재조회 (정렬 우선순위 지정)
    # '대사관'이 들어간 이름을 우선 정렬하기 위해 Case/When을 사용
    embassies = Embassy.objects.filter( # 공관 목록을 필터링
        country_en_name__iexact=country_en  # 영문 국가명이 같은 공관들 필터 (대소문자 구분 X)
    ).annotate( # 정렬 기준을 위한 임시 컬럼 추가
        sort_priority=Case( # sort_priority라는 Case 필드 생성
            When(embassy_name__icontains="대사관", then=Value(0)),  # 대사관 0번째 - 우선
            default=Value(1), # 그외는 모두 1번째
            output_field=IntegerField()
        )
    ).order_by("sort_priority", "embassy_name") # 원하는 정렬 순서 적용

    # 각 공관 데이터를 JSON 형태로 정리
    embassy_list = []
    for e in embassies:
        homepage_url = getattr(e.homepage, "url", None)  # homepage가 없으면 None

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
    category_map = {} # 결과 저장할 딕셔너리
    seen_titles = set()  # 중복 제거용 제목 모음
    for category, keywords in topic_keywords.items(): # 키워드 분류 순회
        q = Q() # 검색 조건 누적용 q 객체
        for kw in keywords:
            q |= Q(content__icontains=kw)  # 키워드가 포함된 공지를 모두 찾음
        matches = base_queryset.filter(q).order_by("-written_dt") # q 조건 적용
        titles = [] # 해당 카테고리의 제목들 저장할 리스트
        for title in matches.values_list("title", flat=True): # 공지 중복 방지 (필터링 된 공지에서 title, content 중 title만 가져옴)
            if title not in seen_titles:
                titles.append(title)
                seen_titles.add(title)
        if titles:
            category_map[category] = titles # 카테고리 딕셔너리에 title 리스트 저장

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

# 국가명별 slug 변수를 확인해볼 수 있는 api 함수
def country_list_api(request):
    countries = Embassy.objects.values("country_name", "country_en_name", "slug").distinct()
    return JsonResponse(list(countries), safe=False)