import axios from "axios";

// 백엔드(FastAPI) 주소를 한 곳에 모아둠 - 나중에 주소 바뀌면 여기만 고치면 됨
const api = axios.create({
  baseURL: "http://localhost:8000/api",
});

export default api;
