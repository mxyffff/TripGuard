const colorMap = {
  caution: '#5398F5',             // 1단계: 여행유의 (파란색)
  warning: '#FCC33C',            // 2단계: 여행자제 (노란색)
  alert: '#FF0000',              // 3단계: 출국권고 (빨간색)
  danger: '#242424',             // 4단계: 여행금지 (검은색)
  STA: 'url(#pattern-hatch)',  // 5단계: 특별여행주의보 (패턴)
};

// alarm_level 숫자별 문자열 변환 함수
function getRiskLevel(levelNum) {
  switch(levelNum) {
    case 1: return 'caution';   // 여행유의
    case 2: return 'warning';   // 여행자제
    case 3: return 'alert';     // 출국권고
    case 4: return 'danger';    // 여행금지
    case 5: return 'STA';       // 특별여행주의보
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
              window.location.href = 'nation.html';
            } else {
              window.location.href = 'cantFind.html';
            }
          });

          // 툴팁 이벤트
          el.addEventListener('mouseenter', () => showTooltip(id));
          el.addEventListener('mouseleave', hideTooltip);
        });
      });
  });

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
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  searchBtn.addEventListener("click", function () {
    const keyword = searchInput.value.trim();

    if (keyword === "중국") {
      window.location.href = "nation.html";
    } else {
      window.location.href = "cantFind.html";
    }
  });
});
