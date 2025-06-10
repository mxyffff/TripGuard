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
  if (menu.style.display === 'none' || menu.style.display === '') {
    menu.style.display = 'flex';
  } else {
    menu.style.display = 'none';
  }
}


// fetch("/reviews/create/china/", {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//   },
//   body: JSON.stringify({
//     content: "미국 정보도 유용해요",
//   }),
// })
//   .then((res) => {
//     if (!res.ok) {
//       throw new Error("서버 오류!");
//     }
//     return res.json();
//   })
//   .then((data) => {
//     console.log("✅ 후기 등록 성공:", data.message);
//     console.log("📝 등록된 리뷰:", data.review);
//   })
//   .catch((err) => {
//     console.error("❌ 후기 등록 실패:", err);
//   });
