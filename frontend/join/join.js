import api from "../api/api.js"; // axios 인스턴스

document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");

  searchBtn.addEventListener("click", function () {
    const keyword = searchInput.value.trim();
    if (keyword === "중국") {
      window.location.href = "../resultPage/result.html";
    } else {
      window.location.href = "/cantFind/cantFind.html";
    }
  });

  const joinBtn = document.querySelector(".btn-primary");
  joinBtn.addEventListener("click", async function () {
    const name = document.getElementById("username").value.trim();
    const nickname = document.getElementById("nickname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const password2 = document.getElementById("passwordConfirm").value.trim();

    // 유효성 체크
    if (!name || !nickname || !email || !password || !password2) {
      alert("모든 항목을 입력해 주세요.");
      return;
    }

    if (password !== password2) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      const response = await api.post("/auth/signup", new URLSearchParams({
        action: "signup",
        email,
        password,
        password2,
        name,
        nickname
      }));

      if (response.data.success) {
        alert("회원가입이 완료되었습니다.");
        window.location.href = "../joinComplete/joinComplete.html";
      } else {
        alert(response.data.message || "회원가입 실패");
      }
    } catch (error) {
      console.error("회원가입 오류:", error);
      alert("서버 오류입니다. 다시 시도해주세요.");
    }
  });
});
