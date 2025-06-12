const colorMap = {
  safe: '#5398F5',
  caution: '#FCC33C',
  STA: 'url(#pattern-hatch)',
  warning: '#EBEBEB',
  danger: '#242424'
};

// ISO 코드 → 위험 등급
const countryRisk = {
  USA: 'safe', CAN: 'safe', MEX: 'caution', BRA: 'caution', ARG: 'caution',
  CHN: 'safe', IND: 'caution', ZAF: 'safe', FRA: 'safe', DEU: 'safe', KOR: 'danger', 
  JPN: 'safe', GBR: 'safe', EGY: 'caution', IRN: 'danger', SYR: 'danger', AFG: 'danger', 
  SAU: 'caution'
};

// ISO 코드 → 한글명 (툴팁용)
const countryNamesKo = {
  USA: '미국', CAN: '캐나다', MEX: '멕시코', BRA: '브라질', ARG: '아르헨티나',
  CHN: '중국', IND: '인도', ZAF: '남아프리카공화국',
  FRA: '프랑스', DEU: '독일', KOR: '대한민국', JPN: '일본', GBR: '영국',
  EGY: '이집트', IRN: '이란', SYR: '시리아', AFG: '아프가니스탄', SAU: '사우디아라비아'
};

fetch("{% static 'assets/world_map_cleaned.svg' %}")
  .then(res => res.text())
  .then(svg => {
    document.getElementById('map-box').innerHTML = svg;

    const svgEl = document.querySelector('#map-box svg');
    svgEl.setAttribute('width', '1268');
    svgEl.style.height = 'auto';

    const allPaths = svgEl.querySelectorAll('path[id]');
    allPaths.forEach(el => {
      const id = el.id;
      const level = countryRisk[id];

      // 색상 지정
      el.setAttribute('fill', level ? colorMap[level] : '#e6e6e6');
      el.style.transition = 'opacity 0.3s';

      el.addEventListener('mouseenter', () => {
        highlightCountry(id);
        showTooltip(id);
      });

      el.addEventListener('mouseleave', () => {
        resetOpacity();
        hideTooltip();
      });

      // 클릭 이벤트 처리
      el.addEventListener('click', () => {
        if (id === 'CHN') {
          // 중국을 클릭했을 때 nation.html 페이지로 이동
          window.location.href = 'nation.html';
        } else {
          // 다른 나라를 클릭했을 때, 예를 들어 오류 페이지로 이동
          window.location.href = 'cantFind.html';
        }
      });
    });
  });
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
  tooltip.innerText = countryNamesKo[code] || code;
  tooltip.style.display = 'block';
}

function hideTooltip() {
  document.getElementById('tooltip').style.display = 'none';
}

document.addEventListener('mousemove', (e) => {
  const tooltip = document.getElementById('tooltip');
  tooltip.style.left = e.pageX + 10 + 'px';
  tooltip.style.top = e.pageY + 10 + 'px';
});

document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  searchBtn.addEventListener("click", function () {
    const keyword = searchInput.value.trim();

    if (keyword === "중국") {
      // 결과 있는 페이지로 이동 (예: result.html 또는 중국 상세 페이지 등)
      window.location.href = "nation.html";
    } else {
      // 결과 없는 페이지로 이동
      window.location.href = "cantFind.html";
    }
  });
});

