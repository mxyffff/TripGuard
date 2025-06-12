import api from "/static/api.js";

// 로그인 함수
const login = async (email, password) => {
    const errorDiv = document.getElementById("error-message");
    errorDiv.textContent="";

    if (!email || !password) {
    errorDiv.textContent = "이메일과 비밀번호를 모두 입력해 주세요.";
    return;
  }

  try {
    const response = await api.post(
      "/auth/api/login/",
      new URLSearchParams({ email, password }) // x-www-form-urlencoded
    );

    if (response.data.success) {
      alert(response.data.message);
      console.log("로그인된 사용자:", response.data.user);
      window.location.href = "/";
    }
  } catch (error) {
    if (error.response?.status === 401) {
      errorDiv.textContent = "이메일 또는 비밀번호가 잘못되었습니다."
    } 
    else {
      errorDiv.textContent = "서버 오류입니다. 다시 시도해 주세요.";
    }
  }
};

// DOM 로드 후 이벤트 등록
document.addEventListener("DOMContentLoaded", () => {
  // 로그인 버튼 이벤트
  const loginBtn = document.getElementById("loginBtn");
  if (loginBtn) {
    loginBtn.addEventListener("click", () => {
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();
      login(email, password);
    });
  }

});
