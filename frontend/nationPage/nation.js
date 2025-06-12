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

async function updateEmbassyTexts() {
  try {
    const res = await fetch(
      "http://localhost:8000/countries/api/detail/china/"
    );
    if (!res.ok) throw new Error("API 요청 실패");

    const data = await res.json();
    const embassies = data.embassies;

    // 카드에 있는 각 대사관 이름에 맞게 업데이트
    document.querySelectorAll(".card[data-name]").forEach((card) => {
      const name = card.getAttribute("data-name");
      const info = embassies.find((e) => e.embassy_name === name);
      if (!info) return;

      const dtList = card.querySelectorAll("dt");

      dtList.forEach((dt) => {
        const label = dt.textContent.trim();
        const dd = dt.nextElementSibling;

        if (label === "주소") dd.textContent = info.address;
        if (label === "전화번호") dd.textContent = info.tel_no;
        if (label === "긴급전화번호" || label === "긴급연락처")
          dd.textContent = info.urgency_tel;
        if (label === "홈페이지") {
          const a = dd.querySelector("a");
          if (a) {
            a.href = info.homepage_url;
            a.textContent = info.homepage_url;
          }
        }
      });
    });
  } catch (err) {
    console.error("대사관 정보 로딩 실패:", err);
    alert("대사관 정보를 불러오지 못했습니다.");
  }
}

updateEmbassyTexts();

const reviewInput = document.getElementById("review-input");
const reviewList = document.getElementById("review-list");

document
  .getElementById("review-submit")
  .addEventListener("click", async function () {
    const content = reviewInput.value.trim(); //Id로 입력칸의  값 가져오기

    // content가 비어 있을 시
    if (!content) {
      alert("후기를 입력해주세요.");
      return;
    }

    try {
      const response = await fetch("/reviews/create/china/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: content }),
      });

      const result = await response.json(); //응답을 js객체로 파싱

      if (response.ok) {
        // 등록 성공 -> 리스트에 추가
        const review = result.review;
        addReview(review);
        reviewInput.value = ""; // 입력칸 비우기
      } else {
        // 에러 -> 실패 메시지
        alert("등록 실패: " + (result.error || result.message));
      }
    } catch (error) {
      console.error("에러 발생:", error);
      alert("요청 실패: 네트워크 오류");
    }
  });

// 후기 등록 (리스트 추가)
function addReview(review) {
  const reviewList = document.getElementById("review-list");
  const date = review.created_at.split(" ")[0].replace(/-/g, ".");

  const item = `
    <div class="review-item" data-review-id="${review.id}"> 
      <div class="user-info">
        <img src="../assets/img/profile.svg" alt="프로필이미지" class="profile-img" />
        <div class="id">${review.nickname}</div>
        <div class="option-wrapper">
          <img
            src="../assets/img/option.svg"
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
          <img src="../assets/img/like.svg" alt="도움이 돼요" />
          ${review.helpfulness}
        </div>
      </span>
      <hr class="review-hr"/>
    </div>
  `;

  reviewList.insertAdjacentHTML("afterbegin", item); // 리스트 맨 위에 추가
}

// 전역 이벤트 리스너 (수정/저장/삭제)
document.getElementById("review-list").addEventListener("click", function (e) {
  if (e.target.classList.contains("edit-btn")) {
    handleEditClick(e.target);
  } else if (e.target.classList.contains("save-mode")) {
    handleSaveClick(e.target);
  } else if (e.target.classList.contains("delete-btn")) {
    handleDeleteClick(e.target);
  }
});

//후기 수정하기
function handleEditClick(button) {
  const reviewItem = button.closest(".review-item"); //클릭된 버튼이 속한 후기블록 찾기
  const contentDiv = reviewItem.querySelector(".review-content");
  const originalContent = contentDiv.textContent; //현재 후기 텍스트를 꺼내서 저장

  contentDiv.innerHTML = `<input type="text" class="edit-input" value="${originalContent}" />`;
  //기존 내용을 수정하도록
  button.textContent = "저장하기"; //수정버튼을 저장버튼으로 변경
  button.classList.add("save-mode"); // 기능 구분용 클래스 추가
}

//후기 저장하기
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
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: newContent }),
    });

    const result = await res.json();

    if (res.ok) {
      const contentDiv = reviewItem.querySelector(".review-content");
      contentDiv.textContent = result.updated_review.content;

      button.textContent = "수정하기";
      button.classList.remove("save-mode");

      alert("후기가 수정되었습니다!");
    } else if (res.status === 403) {
      alert(result.message);
    } else if (res.status === 400) {
      alert(result.error);
    }
  } catch (err) {
    alert("수정 요청 실패: 네트워크 오류");
  }
}

//후기 삭제하기
async function handleDeleteClick(button) {
  const reviewItem = button.closest(".review-item");
  const reviewId = reviewItem.dataset.reviewId;

  const confirmDelete = confirm("정말 삭제하시겠습니까?");
  if (!confirmDelete) return;

  try {
    const res = await fetch(`/reviews/delete/${reviewId}/`, {
      method: "POST",
    });
    const result = await res.json();

    if (res.ok) {
      alert(result.message);
      reviewItem.remove();
    } else {
      alert(result.message);
    }
  } catch (err) {
    console.error("삭제 요청 실패:", err);
    alert("삭제 요청 실패: 네트워크 오류");
  }
}

//기존 후기 목록
const reviewData = [
  {
    userId: "kali***",
    content: "베이징에서 소매치기 당할 뻔 했어요! 조심하세요!",
    date: "2025.05.06",
    likes: 35,
  },
  {
    userId: "nana***",
    content: "왕푸징 근처에서 휴대폰 도난당했어요...ㅠㅠ",
    date: "2025.04.30",
    likes: 12,
  },
  {
    userId: "jay***",
    content: "우다코 지하철에서 수상한 사람들 조심하세요.",
    date: "2025.03.28",
    likes: 8,
  },
  {
    userId: "sejin***",
    content: "심야에 택시앱 이용할 때는 꼭 차량번호 확인하고 탑승하세요.",
    date: "2025.05.09",
    likes: 27,
  },
  {
    userId: "taemin***",
    content:
      "번화가에서 경찰이 여권 검사할 수 있으니 항상 사진이라도 소지하세요. 불심검문에 대비하면 좋아요!",
    date: "2025.05.07",
    likes: 31,
  },
];

reviewData.forEach((review) => {
  const item = `
    <div class="review-item" >
      <div class="user-info">
        <img src="../assets/img/profile.svg" alt="프로필이미지" class="profile-img" />
        <div class="id">${review.userId}</div>
        <div class="option-wrapper">
          <img
            src="../assets/img/option.svg"
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
        <div class="review-date">${review.date}</div>
        <div class="likes">
          도움이 돼요
          <img src="../assets/img/like.svg" alt="도움이 돼요" />
          ${review.likes}
        </div>
      </span>
      <hr class="review-hr"/>
    </div>
  `;
  reviewList.innerHTML += item;
});

//로그인 안한 경우 후기리스트 블러 처리
document.addEventListener("DOMContentLoaded", async function () {
  try {
    const res = await fetch("/countries/api/detail/china/");
    const data = await res.json();

    if (!data.is_authenticated) {
      document.getElementById("review-list").classList.add("blurred");
      document.getElementById("login-required").style.display = "block";
    }
  } catch (err) {
    console.error("데이터 로딩 실패:", err);
  }
});

//좋아요 버튼(도움이돼요)
document.addEventListener("click", async (e) => {
  const likesBtn = e.target.closest(".likes");
  if (!likesBtn) return;

  const wrapper = likesBtn.closest(".info-wrap");
  const reviewId = wrapper.dataset.reviewId;

  try {
    const res = await fetch(`/reviews/helpful/${reviewId}/`, {
      method: "POST",
    });
    const result = await res.json();

    if (res.ok) {
      likesEl.querySelector(".helpfulness-count").textContent =
        result.helpfulness_count;
    } else {
      alert(result.message);
    }
  } catch (err) {
    console.error("도움 요청 실패:", err);
    alert("네트워크 오류");
  }
});

//안전공지
document.addEventListener("DOMContentLoaded", async function () {
  try {
    const res = await fetch("/countries/api/detail/china/");
    const data = await res.json();

    // 현재 사용자의 닉네임 표시(리뷰부분)
    if (data.is_authenticated && data.nickname) {
      document.querySelector(".review-input .id").textContent = data.nickname;
    }
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
    console.error("안전공지 로딩 실패:", err);
  }
});
