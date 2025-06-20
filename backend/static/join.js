import api from "/static/api.js"; // axios 인스턴스

document.addEventListener("DOMContentLoaded", function () {
  const searchBtn = document.getElementById("searchBtn");
  const searchInput = document.getElementById("searchInput");


   // 이메일 중복 확인을 위한 입력 이벤트
  const emailInput = document.getElementById("email");
  const emailStatus = document.getElementById("emailStatus");

  // 이메일 입력 시 실시간으로 중복 확인
  emailInput.addEventListener("input", async function () {
    const email = emailInput.value.trim();

    if (!email) {
      emailStatus.textContent = "";
      return;
    }

    try {
      const response = await api.post("/auth/api/signup/", new URLSearchParams({
        action: "check_email",
        email
      }));

      if (response.data.success) {
        emailStatus.textContent = "사용 가능한 이메일입니다.";
        emailStatus.style.color = "green";
      } else {
        emailStatus.textContent = response.data.message || "이미 사용 중인 이메일입니다.";
        emailStatus.style.color = "red";
      }
    } catch (error) {
      console.error("이메일 중복 확인 오류:", error);
      emailStatus.textContent = "서버 오류입니다. 다시 시도해 주세요.";
      emailStatus.style.color = "red";
    }
  });

  // 비밀번호 일치 확인을 위한 함수
  async function checkPasswordMatch(password, password2) {
    try {
      const response = await api.post("/auth/api/signup/", new URLSearchParams({
        action: "check_password",
        password,
        password2,
      }));
      return response.data.success;
    } catch (error) {
      console.error("비밀번호 일치 확인 오류: ", error);
      return false;
    }
  }

  // 회원가입 버튼 이벤트
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

    const passwordChecked = await checkPasswordMatch(password, password2);
    if (!passwordChecked) {
      alert("비밀번호가 일치하지 않습니다.");
      return;
    }

    try {
      const response = await api.post("/auth/api/signup/", new URLSearchParams({
        action: "signup",
        email,
        password,
        password2,
        name,
        nickname
      }));

      if (response.data.success) {
        alert("회원가입이 완료되었습니다.");
        window.location.href = "/auth/signup/complete/";
      } else {
        alert(response.data.message || "회원가입 실패");
      }
    } catch (error) {
      console.error("회원가입 오류: ", error);
      alert("서버 오류입니다. 다시 시도해 주세요.");
    }
  });
});