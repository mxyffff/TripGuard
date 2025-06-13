const api = axios.create({
  baseURL: "http://127.0.0.1:8000",  // 그냥 직접 주소 적기
  withCredentials: true,
});

export default api;