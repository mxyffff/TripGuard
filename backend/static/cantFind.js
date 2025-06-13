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
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            const res = await fetch("/auth/logout/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                },
                credentials: "include",
            });

            if (res.ok) {
                // 그냥 현재 페이지 그대로 유지하면서 세션만 갱신!
                window.location.reload();
            } else {
                alert("로그아웃 실패");
            }
        });
    }
});