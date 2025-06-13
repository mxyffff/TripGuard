{% load static %}
<script>
const colorMap = {
  safe: '#5398F5',      // 예: 0 또는 기본
  caution: '#FCC33C',   // 1
  STA: 'url(#pattern-hatch)', // 5
  warning: '#EBEBEB',   // 3
  danger: '#242424'     // 2, 4 등 위험 단계
};

// alarm_level 숫자별 문자열 매핑
function getRiskLevel(levelNum) {
  switch(levelNum) {
    case 1: return 'caution';
    case 2: return 'danger';
    case 3: return 'warning';
    case 4: return 'danger';
    case 5: return 'STA';
    default: return 'safe';
  }
}

// 강조 및 툴팁 관련 함수들
function highlightCountry(targetId) {
  const paths = document.querySelectorAll('#map-box path[id]');
  paths.forEach(p => {
    p.style.opacity = (p.id === targetId) ? '1' : '0.2';
  });
}

function resetOpacity() {
  const paths = document.querySelectorAll('#map-box path[id]');
  paths.forEach(p => {
    p.style.opacity = '1';
  });
}

function showTooltip(code) {
  const tooltip = document.getElementById('tooltip');
  tooltip.innerText = (typeof countryNamesKo !== 'undefined' && countryNamesKo[code]) ? countryNamesKo[code] : code;
  tooltip.style.display = 'block';
}

function hideTooltip() {
  const tooltip = document.getElementById('tooltip');
  if(tooltip) tooltip.style.display = 'none';
}

document.addEventListener("DOMContentLoaded", function () {
  fetch("{% static 'assets/world_map_cleaned.svg' %}")
    .then(res => res.text())
    .then(svgText => {
      const mapBox = document.getElementById("map-box");
      mapBox.innerHTML = svgText;

      const svgEl = mapBox.querySelector("svg");
      if (!svgEl) {
        console.error("SVG가 삽입되지 않았습니다!");
        return;
      }

      svgEl.style.width = "100%";
      svgEl.style.height = "100%";
      svgEl.style.display = "block";

      // 경로들 가져오기
      const paths = svgEl.querySelectorAll('path[id]');

      // 기본 fill 설정
      paths.forEach(path => {
        if (!path.getAttribute('fill') || path.getAttribute('fill') === 'none') {
          path.setAttribute('fill', '#e6e6e6');
        }
        path.style.transition = 'opacity 0.3s';
      });

      // GeoJSON fetch 및 색칠
      fetch("/api/alert_geojson/")
        .then(res => res.json())
        .then(data => {
          const countryRisk = {};
          data.features.forEach(feature => {
            const code = feature.properties.country_code;
            const levelNum = feature.properties.alarm_level;
            countryRisk[code] = getRiskLevel(levelNum);
          });

          paths.forEach(el => {
            const id = el.id;
            const level = countryRisk[id];
            el.setAttribute('fill', level ? colorMap[level] : '#e6e6e6');

            el.addEventListener('mouseenter', () => {
              highlightCountry(id);
              showTooltip(id);
            });
            el.addEventListener('mouseleave', () => {
              resetOpacity();
              hideTooltip();
            });
            el.addEventListener('click', () => {
              window.location.href = `/alerts/${id}/`;
            });
          });
        })
        .catch(e => console.error('GeoJSON fetch error:', e));
    })
    .catch(err => {
      console.error("SVG fetch 실패:", err);
    });

  // 검색 기능
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");
  if (searchBtn && searchInput) {
    searchBtn.addEventListener("click", function () {
      const keyword = searchInput.value.trim();
      if (keyword === "중국") {
        window.location.href = "nation.html";
      } else {
        window.location.href = "cantFind.html";
      }
    });
  }
});

document.addEventListener('mousemove', (e) => {
  const tooltip = document.getElementById('tooltip');
  if(tooltip) {
    tooltip.style.left = e.pageX + 10 + 'px';
    tooltip.style.top = e.pageY + 10 + 'px';
  }
});
</script>
