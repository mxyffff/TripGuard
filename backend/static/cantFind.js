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