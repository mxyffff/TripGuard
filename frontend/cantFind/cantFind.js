document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  searchBtn.addEventListener("click", function () {
    const keyword = searchInput.value.trim();

    if (keyword === "중국") {
      // 결과 있는 페이지로 이동 (예: result.html 또는 중국 상세 페이지 등)
      window.location.href = "../resultPage/result.html"; 
    } else {
      // 결과 없는 페이지로 이동
      window.location.href = "cantFind.html";
    }
  });
});