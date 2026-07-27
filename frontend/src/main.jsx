import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./index.css";
import App from "./App.jsx";

// 이 파일이 리액트 앱의 진입점(entry point) - index.html의 <div id="root">에 App을 그려 넣음
// BrowserRouter로 감싸야 App.jsx 안에서 Routes/Link 같은 라우팅 기능을 쓸 수 있음
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
);
