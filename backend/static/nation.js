function showTab(tabId, clickedTab) {
    document.querySelectorAll(".tab").forEach((el) => {
        el.style.display = "none"; //클릭시 모든 탭 가리기
    });
    document.getElementById(tabId).style.display = "block"; //클릭된 탭 내용만 보이도록

    document.querySelectorAll(".select.active").forEach((tab) => {
        tab.classList.remove("active"); //active상태인 탭 요소에 active 제거
    });
    clickedTab.classList.add("active"); //클릭된 탭 요소에 active 상태 추가
}

function toggleOptions(el) {
    const menu = el.nextElementSibling;
    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "flex";
    } else {
        menu.style.display = "none";
    }
}

//🔧 재외공관 api 연결
async function updateEmbassyTexts() {
    try {
        const res = await fetch("http://localhost:8000/countries/api/detail/china/");
        if (!res.ok) throw new Error("API 요청 실패");

        const data = await res.json();
        const embassies = data.embassies;

        const container = document.getElementById("embassy-cards");
        container.innerHTML = ""; // 초기화

        // 🔧 공관명 키워드에 따른 지도 이미지 파일명 매핑
        const mapImageMap = {
            "대사관": "embassy1.png",
            "홍콩": "embassy2.png",
            "상하이": "embassy3.png",
            "칭다오": "embassy4.png"
        };

        embassies.forEach((info, index) => {
            const card = document.createElement("div");
            card.className = "card";

            // 🔧 공관 이름에 따라 지도 이미지 파일 선택
            let imageFile = "embassy1.png"; // 기본값
            for (const keyword in mapImageMap) {
                if (info.embassy_name.includes(keyword)) {
                    imageFile = mapImageMap[keyword];
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
            <a href="https://maps.app.goo.gl/9WQgEg81u1nZJtjJA" target="_blank">
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

const reviewInput = document.getElementById("review-input");
const reviewList = document.getElementById("review-list");

document.getElementById("review-submit").addEventListener("click", async function () {
    const content = reviewInput.value.trim(); // Id로 입력칸의 값 가져오기

    if (!content) {
        alert("후기를 입력해주세요.");
        return;
    }

    try {
        const response = await fetch("/reviews/create/china/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json", // 🔧 JSON 전송
            },
            body: JSON.stringify({content}), // 🔧 문자열화
        });

        const result = await response.json();

        if (response.ok) {
            const review = result.review;
            addReview(review);
            reviewInput.value = "";
        } else {
            alert("등록 실패: " + (result.error || result.message));
        }
    } catch (error) {
        console.error("에러 발생:", error);
        alert("요청 실패: 네트워크 오류");
    }
});

// 후기 등록 (리스트 추가)
function addReview(review) {
    const date = review.created_at.split(" ")[0].replace(/-/g, ".");

    const item = `
    <div class="review-item" data-review-id="${review.id}"> 
      <div class="user-info">
        <img src="/static/assets/img/profile.svg" alt="프로필이미지" class="profile-img" />
        <div class="id">${review.nickname}</div>
        <div class="option-wrapper">
          <img
            src="/static/assets/img/option.svg"
            alt="옵션"
            class="review-option"
            onclick="toggleOptions(this)"
          />
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
          <img src="/static/assets/img/like.svg" alt="도움이 돼요" />
          ${review.helpfulness}
        </div>
      </span>
      <hr class="review-hr"/>
    </div>
  `;
    reviewList.insertAdjacentHTML("afterbegin", item);
}

// 전역 이벤트 리스너 (수정/저장/삭제)
document.getElementById("review-list").addEventListener("click", function (e) {
    if (e.target.classList.contains("edit-btn") && !e.target.classList.contains("save-mode")) {
        handleEditClick(e.target);
    } else if (e.target.classList.contains("save-mode")) {
        handleSaveClick(e.target);
    } else if (e.target.classList.contains("delete-btn")) {
        handleDeleteClick(e.target);
    } else if (e.target.closest(".likes")) {
        handleHelpfulnessClick(e.target.closest(".review-item")); // ✅ "도움이 돼요" 처리 추가
    }
});

// 후기 수정하기
function handleEditClick(button) {
    const reviewItem = button.closest(".review-item");
    const contentDiv = reviewItem.querySelector(".review-content");
    const originalContent = contentDiv.textContent;

    contentDiv.innerHTML = `<input type="text" class="edit-input" value="${originalContent}" />`;
    button.textContent = "저장하기";
    button.classList.add("save-mode"); // 🔧 저장 모드 추가
}

// 후기 저장하기
async function handleSaveClick(button) {
    const reviewItem = button.closest(".review-item");
    const input = reviewItem.querySelector(".edit-input");
    const reviewId = reviewItem.dataset.reviewId;
    const newContent = input.value.trim();

    if (!newContent) {
        alert("수정할 내용을 입력해주세요.");
        return;
    }

    try {
        const res = await fetch(`/reviews/update/${reviewId}/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"}, // 🔧 JSON 포맷
            body: JSON.stringify({content: newContent}), // 🔧 문자열화
        });

        const result = await res.json();

        if (res.ok) {
            const contentDiv = reviewItem.querySelector(".review-content");
            contentDiv.textContent = result.updated_review.content;

            button.textContent = "수정하기";
            button.classList.remove("save-mode");

            alert("후기가 수정되었습니다!");
        } else {
            alert(result.message || result.error);
        }
    } catch (err) {
        alert("수정 요청 실패: 네트워크 오류");
    }
}

// 후기 삭제하기
async function handleDeleteClick(button) {
    const reviewItem = button.closest(".review-item");
    const reviewId = reviewItem.dataset.reviewId;

    const confirmDelete = confirm("정말 삭제하시겠습니까?");
    if (!confirmDelete) return;

    try {
        const res = await fetch(`/reviews/delete/${reviewId}/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
        });
        const result = await res.json();

        if (res.ok) {
            alert(result.message);
            reviewItem.remove();
        } else {
            alert(result.message || result.error);
        }
    } catch (err) {
        console.error("삭제 요청 실패:", err);
        alert("삭제 요청 실패: 네트워크 오류");
    }
}

// 도움이 돼요 클릭 이벤트
reviewList.addEventListener("click", async function (e) {
    if (e.target.closest(".likes")) {
        const reviewItem = e.target.closest(".review-item");
        const reviewId = reviewItem.dataset.reviewId;

        try {
            const res = await fetch(`/reviews/helpful/${reviewId}/`, {
                method: "POST",
            });

            const result = await res.json();

            if (res.ok) {
                const likesDiv = reviewItem.querySelector(".likes");
                likesDiv.innerHTML = `
          도움이 돼요
          <img src="/static/assets/img/like.svg" alt="도움이 돼요" />
          ${result.helpfulness_count}
        `;
            } else if (res.status === 403) {
                alert(result.error); // ✅ 여기에 정확한 메시지 출력됨
            } else {
                alert("도움 요청 실패: 서버 오류");
            }
        } catch (err) {
            console.error("도움 요청 실패:", err);
            alert("도움 요청 실패: 네트워크 오류");
        }
    }
});

// 로그인 여부 확인 + 닉네임 및 안전공지 + 후기 목록 로딩
document.addEventListener("DOMContentLoaded", async function () {
    try {
        const res = await fetch("/countries/api/detail/china/");
        const data = await res.json();

        if (!data.is_authenticated) {
            document.getElementById("review-list").classList.add("blurred");
            document.getElementById("login-required").style.display = "block";
        }

        if (data.is_authenticated && data.nickname) {
            document.querySelector(".review-input .id").textContent = data.nickname;
        }

        // ✅ 후기 리스트 초기 로딩
        const reviews = data.reviews;
        reviewList.innerHTML = "";
        reviews.forEach((review) => addReview(review));

        // ✅ 안전 공지사항 불러오기
        const safetyList = data.country_safeties;
        const table = document.querySelector(".notice-table");

        safetyList.forEach((item) => {
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