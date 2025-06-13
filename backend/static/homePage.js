const colorMap = {
    caution: '#5398F5',             // 1단계: 여행유의 (파란색)
    warning: '#FCC33C',            // 2단계: 여행자제 (노란색)
    alert: '#FF0000',              // 3단계: 출국권고 (빨간색)
    danger: '#242424',             // 4단계: 여행금지 (검은색)
    STA: 'url(#pattern-hatch)',  // 5단계: 특별여행주의보 (패턴)
};

// alarm_level 숫자별 문자열 변환 함수
function getRiskLevel(levelNum) {
    switch (levelNum) {
        case 1:
            return 'caution';   // 여행유의
        case 2:
            return 'warning';   // 여행자제
        case 3:
            return 'alert';     // 출국권고
        case 4:
            return 'danger';    // 여행금지
        case 5:
            return 'STA';       // 특별여행주의보
    }
}

// SVG 불러와서 지도에 표시 + 위험도 색칠 + 이벤트 등록
fetch("/static/assets/img/world_map_cleaned.svg")
    .then(res => res.text())
    .then(svgText => {
        document.getElementById("map-box").innerHTML = svgText;
        const svgEl = document.querySelector('#map-box svg');

        fetch("/api/alert_geojson/")
            .then(res => res.json())
            .then(data => {
                const countryRisk = {};
                data.features.forEach(feature => {
                    countryRisk[feature.properties.country_code] = getRiskLevel(feature.properties.alarm_level);
                });

                const allPaths = svgEl.querySelectorAll('path[id]');
                allPaths.forEach(el => {
                    const id = el.id;
                    const level = countryRisk[id];
                    el.setAttribute('fill', level ? colorMap[level] : '#e6e6e6');
                    el.style.transition = 'opacity 0.3s';

                    // 클릭 이벤트
                    el.addEventListener('click', () => {
                        if (id === 'CN') {
                            window.location.href = '/nation/';
                        } else {
                            window.location.href = '/cantFind/';
                        }
                    });

                    // 툴팁 이벤트
                    el.addEventListener('mouseenter', () => showTooltip(id));
                    el.addEventListener('mouseleave', hideTooltip);
                });
            });
    });

const countryNamesKo = {
    IL: "이스라엘", IT: "이탈리아", TM: "투르크메니스탄", IN: "인도", JM: "자메이카",
    ZM: "잠비아", GQ: "적도 기니", DJ: "지부티", ZW: "짐바브웨", CL: "칠레",
    TD: "차드", CM: "카메룬", KH: "캄보디아", KE: "케냐", PY: "파라과이",
    PG: "파푸아뉴기니", PL: "폴란드", FR: "프랑스", FJ: "피지", CH: "스위스",
    MR: "모리타니", MY: "말레이시아", MW: "말라위", MH: "마셜 제도", MG: "마다가스카르",
    LI: "리히텐슈타인", LY: "리비아", RW: "르완다", GR: "그리스", IE: "아일랜드",
    SE: "스웨덴", OM: "오만", EG: "이집트", PT: "포르투갈", TN: "튀니지",
    RU: "러시아", GB: "영국", UA: "우크라이나", DE: "독일", ES: "스페인",
    IT: "이탈리아", PL: "폴란드", CZ: "체코", AT: "오스트리아", NL: "네덜란드",
    BE: "벨기에", CH: "스위스", DK: "덴마크", NO: "노르웨이", FI: "핀란드",
    HU: "헝가리", SK: "슬로바키아", BG: "불가리아", RO: "루마니아", HR: "크로아티아",
    RS: "세르비아", LT: "리투아니아", LV: "라트비아", EE: "에스토니아", CY: "키프로스",
    MT: "몰타", IS: "아이슬란드", LU: "룩셈부르크", MD: "몰도바", AL: "알바니아",
    ME: "몬테네그로", BA: "보스니아 헤르체고비나", MK: "북마케도니아", GE: "조지아", AZ: "아제르바이잔",
    AM: "아르메니아", BY: "벨라루스", KZ: "카자흐스탄", TJ: "타지키스탄", UZ: "우즈베키스탄",
    TM: "투르크메니스탄", KG: "키르기스스탄", AF: "아프가니스탄", PK: "파키스탄", BD: "방글라데시",
    NP: "네팔", BT: "부탄", LK: "스리랑카", MV: "몰디브", IR: "이란",
    IQ: "이라크", SY: "시리아", JO: "요르단", LB: "레바논", SA: "사우디아라비아",
    YE: "예멘", AE: "아랍에미리트", QA: "카타르", BH: "바레인", KW: "쿠웨이트",
    OM: "오만", EG: "이집트", SD: "수단", LY: "리비아", TN: "튀니지",
    DZ: "알제리", MA: "모로코", EH: "서사하라", ZW: "짐바브웨", ZA: "남아프리카 공화국",
    NA: "나미비아", BW: "보츠와나", MZ: "모잠비크", MW: "말라위", ZM: "잠비아",
    AO: "앙골라", CD: "콩고 민주 공화국", CG: "콩고 공화국", GA: "가봉", CM: "카메룬",
    CF: "중앙아프리카 공화국", TD: "차드", SD: "수단", ET: "에티오피아", SO: "소말리아",
    KE: "케냐", UG: "우간다", RW: "르완다", BI: "부룬디", TZ: "탄자니아",
    MG: "마다가스카르", RE: "레위니옹", MU: "모리셔스", SC: "세이셸", KM: "코모로",
    CN: "중국", KR: "대한민국", US: "미국", JP: "일본", SO: "소말리아", SB: "솔로몬 제도",
    FJ: "피지", SR: "수리남", LK: "스리랑카", ES: "스페인", SI: "슬로베니아", SY: "시리아",
    SL: "시에라리온", AM: "아르메니아", AU: "오스트레일리아", AR: "아르헨티나", HT: "아이티",
    MN: "몽골", PF: "프랑스령 폴리네시아",
};

// 툴팁 관련 함수
function showTooltip(code) {
    const tooltip = document.getElementById('tooltip');
    tooltip.innerText = countryNamesKo[code] || code;
    tooltip.style.display = 'block';
}

function hideTooltip() {
    document.getElementById('tooltip').style.display = 'none';
}

// 툴팁 위치 마우스 따라 이동
document.addEventListener('mousemove', (e) => {
    const tooltip = document.getElementById('tooltip');
    tooltip.style.left = e.pageX + 10 + 'px';
    tooltip.style.top = e.pageY + 10 + 'px';
});

// 검색 버튼 이벤트 (DOMContentLoaded 안에)
document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("searchBtn");
    const input = document.getElementById("searchInput");

    function handleSearch() {
        const keyword = input.value.trim();
        if (keyword === "중국") {
            window.location.href = "/nation/";
        } else {
            window.location.href = "/cantFind/";
        }
    }

    // 1. 버튼 클릭 시 검색
    if (btn) {
        btn.addEventListener("click", handleSearch);
    }

    // 2. 엔터 키 입력 시 검색
    if (input) {
        input.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                handleSearch();
            }
        });
    }

    const logoutBtn = document.getElementById("logout-btn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", async () => {
            const res = await fetch("{% url 'users:logout' %}", {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}", // 템플릿 내 csrf 토큰 사용
                },
            });

            if (res.ok) {
                location.reload(); // 페이지 다시 로드해서 로그인 상태 반영
            } else {
                alert("로그아웃 실패");
            }
        });
    }
});