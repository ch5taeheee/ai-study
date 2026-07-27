import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import SmartScanner from "./pages/SmartScanner";
import ChatBot from "./pages/ChatBot";
import MenuBot from "./pages/MenuBot";
import TestLab from "./pages/TestLab";

// 이 앱의 페이지 주소(URL)들을 여기서 전부 정의함
// 예전 Streamlit은 session_state['current_page'] 값으로 화면을 바꿨는데,
// React에서는 이렇게 URL 경로 기준으로 화면을 나누는 게 표준 방식(react-router)
export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<Login />} />
        {/* 로그인 필요한 페이지들은 ProtectedRoute로 한 번씩 감싸줌 */}
        <Route
          path="/scanner"
          element={
            <ProtectedRoute>
              <SmartScanner />
            </ProtectedRoute>
          }
        />
        <Route
          path="/chatbot"
          element={
            <ProtectedRoute>
              <ChatBot />
            </ProtectedRoute>
          }
        />
        <Route
          path="/menu"
          element={
            <ProtectedRoute>
              <MenuBot />
            </ProtectedRoute>
          }
        />
        <Route
          path="/test"
          element={
            <ProtectedRoute>
              <TestLab />
            </ProtectedRoute>
          }
        />
        {/* 정의 안 된 경로로 들어오면 로그인 페이지로 */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </AuthProvider>
  );
}
