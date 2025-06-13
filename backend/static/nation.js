// 탭 전환 기능
function showTab(tabId, clickedTab) {
    document.querySelectorAll(".tab").forEach((el) => {
        el.style.display = "none"; // 모든 탭 숨기기
    });
    document.getElementById(tabId).style.display = "block"; // 선택된 탭 보이기

    document.querySelectorAll(".select.active").forEach((tab) => {
        tab.classList.remove("active"); // 기존 active 제거
    });
    clickedTab.classList.add("active"); // 현재 탭 active 추가
}

// 옵션 메뉴 토글 (후기 옵션 버튼)
function toggleOptions(el) {
    const menu = el.nextElementSibling;
    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "flex";
    } else {
        menu.style.display = "none";
    }
}

// 재외공관 정보 로딩
async function updateEmbassyTexts() {
    try {
        const res = await fetch("http://localhost:8000/countries/api/detail/china/");
        if (!res.ok) throw new Error("API 요청 실패");

        const data = await res.json();
        const embassies = data.embassies;
        const container = document.getElementById("embassy-cards");
        container.innerHTML = "";

        const mapImageMap = {
            "대사관": "embassy1.png",
            "홍콩": "embassy2.png",
            "상하이": "embassy3.png",
            "칭다오": "embassy4.png"
        };
        const mapLinkMap = {
            "대사관": "https://maps.app.goo.gl/9WQgEg81u1nZJtjJA",
            "홍콩": "https://maps.app.goo.gl/6DqfBKdtdTMniQks8",
            "상하이": "https://maps.app.goo.gl/NTNdPD5wx3u5jGez8",
            "칭다오": "https://maps.app.goo.gl/74to7wzQxCBzJc8Z8"
        };

        embassies.forEach((info) => {
            const card = document.createElement("div");
            card.className = "card";

            let imageFile = "embassy1.png";
            let mapLink = mapLinkMap["대사관"];

            for (const keyword in mapImageMap) {
                if (info.embassy_name.includes(keyword)) {
                    imageFile = mapImageMap[keyword];
                    mapLink = mapLinkMap[keyword];
                    break;
                }
            }

            card.innerHTML = `
                <h2>🏛️${info.embassy_name}</h2>
                <span class="embassy-wrap">
                    <dl class="embassy-list">
                        <div class="embassy-item"><dt>주소</dt><dd>${info.address || "정보 없음"}</dd></div>
                        <div class="embassy-item"><dt>전화번호</dt><dd>${info.tel_no || "정보 없음"}</dd></div>
                        <div class="embassy-item"><dt>긴급전화번호</dt><dd>${info.urgency_tel || "정보 없음"}</dd></div>
                        <div class="embassy-item"><dt>홈페이지</dt><dd><a href="${info.homepage_url || '#'}" target="_blank">${info.homepage_url ? "바로가기" : "정보 없음"}</a></dd></div>
                    </dl>
                    <div class="embassy-map">
                        <a href="${mapLink}" target="_blank">
                            <img src="/static/assets/img/${imageFile}" alt="지도이미지"/>
                        </a>
                    </div>
                </span>
            `;
            container.appendChild(card);
        });
    } catch (err) {
        console.error("대사관 정보 로딩 실패:", err);
        alert("대사관 정보를 불러오지 못했습니다.");
    }
}

updateEmbassyTexts();

// 유의지역 공지 탭 내용
document.addEventListener("DOMContentLoaded", async function () {
    try {
        const res = await fetch("/countries/api/detail/china/");
        const data = await res.json();
        const categoryMap = data.category_map;
        const dangerSection = document.getElementById("danger");

        for (const category in categoryMap) {
            const title = document.createElement("h2");
            title.textContent = `${category} 유의지역`;
            dangerSection.appendChild(title);

            const contentWrapper = document.createElement("div");
            contentWrapper.classList.add("danger-content");

            categoryMap[category].forEach((item) => {
                const p = document.createElement("p");
                p.textContent = `- ${item}`;
                contentWrapper.appendChild(p);
            });

            dangerSection.appendChild(contentWrapper);

            const hr = document.createElement("hr");
            hr.classList.add("danger-hr");
            dangerSection.appendChild(hr);
        }
    } catch (err) {
        console.error("유의지역 로딩 실패:", err);
    }
});

// 후기 작성
const reviewInput = document.getElementById("review-input");
const reviewList = document.getElementById("review-list");

document.getElementById("review-submit").addEventListener("click", async function () {
    const content = reviewInput.value.trim();
    if (!content) return alert("후기를 입력해주세요.");

    try {
        const response = await fetch("/reviews/create/china/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({content}),
        });
        const result = await response.json();

        if (response.ok) {
            addReview(result.review);
            reviewInput.value = "";
        } else {
            alert("등록 실패: " + (result.error || result.message));
        }
    } catch (error) {
        alert("요청 실패: 네트워크 오류");
    }
});

// 후기 출력
function addReview(review) {
    const date = review.created_at.split(" ")[0].replace(/-/g, ".");

    const item = `
        <div class="review-item" data-review-id="${review.id}">
            <div class="user-info">
                <img src="/static/assets/img/profile.svg" class="profile-img" />
                <div class="id">${review.nickname}</div>
                <div class="option-wrapper">
                    <img src="/static/assets/img/option.svg" class="review-option" onclick="toggleOptions(this)" />
                    <div class="option-menu" style="display: none">
                        <button class="edit-btn">수정하기</button>
                        <button class="delete-btn">삭제하기</button>
                    </div>
                </div>
            </div>
            <div class="review-content">${review.content}</div>
            <span class="info-wrap">
                <div class="review-date">${date}</div>
                <div class="likes">
                    도움이 돼요
                    <img src="/static/assets/img/like.svg" />
                    ${review.helpfulness}
                </div>
            </span>
            <hr class="review-hr"/>
        </div>
    `;
    reviewList.insertAdjacentHTML("afterbegin", item);
}

// 후기 수정 / 저장 / 삭제 / 도움이 돼요 이벤트
document.getElementById("review-list").addEventListener("click", function (e) {
    const target = e.target;
    if (target.classList.contains("edit-btn") && !target.classList.contains("save-mode")) {
        handleEditClick(target);
    } else if (target.classList.contains("save-mode")) {
        handleSaveClick(target);
    } else if (target.classList.contains("delete-btn")) {
        handleDeleteClick(target);
    } else if (target.closest(".likes")) {
        handleHelpfulnessClick(target.closest(".review-item"));
    }
});

// 후기 수정
function handleEditClick(button) {
    const reviewItem = button.closest(".review-item");
    const contentDiv = reviewItem.querySelector(".review-content");
    const originalContent = contentDiv.textContent;

    contentDiv.innerHTML = `<input type="text" class="edit-input" value="${originalContent}" />`;
    button.textContent = "저장하기";
    button.classList.add("save-mode");
}

// 후기 저장
async function handleSaveClick(button) {
    const reviewItem = button.closest(".review-item");
    const input = reviewItem.querySelector(".edit-input");
    const newContent = input.value.trim();
    const reviewId = reviewItem.dataset.reviewId;

    if (!newContent) return alert("수정할 내용을 입력해주세요.");

    try {
        const res = await fetch(`/reviews/update/${reviewId}/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({content: newContent}),
        });
        const result = await res.json();

        if (res.ok) {
            reviewItem.querySelector(".review-content").textContent = result.updated_review.content;
            button.textContent = "수정하기";
            button.classList.remove("save-mode");
            alert("후기가 수정되었습니다!");
        } else {
            alert(result.message || result.error);
        }
    } catch {
        alert("수정 실패: 네트워크 오류");
    }
}

// 후기 삭제
async function handleDeleteClick(button) {
    const reviewItem = button.closest(".review-item");
    const reviewId = reviewItem.dataset.reviewId;
    if (!confirm("정말 삭제하시겠습니까?")) return;

    try {
        const res = await fetch(`/reviews/delete/${reviewId}/`, {method: "POST"});
        const result = await res.json();

        if (res.ok) {
            alert(result.message);
            reviewItem.remove();
        } else {
            alert(result.message || result.error);
        }
    } catch {
        alert("삭제 실패: 네트워크 오류");
    }
}

// 도움이 돼요
async function handleHelpfulnessClick(reviewItem) {
    const reviewId = reviewItem.dataset.reviewId;

    try {
        const res = await fetch(`/reviews/helpful/${reviewId}/`, {method: "POST"});
        const result = await res.json();

        if (res.ok) {
            reviewItem.querySelector(".likes").innerHTML = `
                도움이 돼요
                <img src="/static/assets/img/like.svg" />
                ${result.helpfulness_count}
            `;
        } else if (res.status === 403) {
            alert(result.error);
        } else {
            alert("도움 요청 실패: 서버 오류");
        }
    } catch {
        alert("도움 요청 실패: 네트워크 오류");
    }
}

// 초기 로딩: 후기/로그인상태/공지사항
document.addEventListener("DOMContentLoaded", async function () {
    try {
        const res = await fetch("/countries/api/detail/china/");
        const data = await res.json();

        if (!data.is_authenticated) {
            reviewList.classList.add("blurred");
            document.getElementById("login-required").style.display = "block";
        } else if (data.nickname) {
            document.querySelector(".review-input .id").textContent = data.nickname;
        }

        reviewList.innerHTML = "";
        data.reviews.forEach(addReview);

        const table = document.querySelector(".notice-table");
        data.country_safeties.forEach((item) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td class="tag-notice">안내</td>
                <td class="title">${item.title}</td>
                <td class="date">${item.written_dt}</td>
            `;
            table.appendChild(row);
        });
    } catch (err) {
        console.error("데이터 로딩 실패:", err);
    }
});