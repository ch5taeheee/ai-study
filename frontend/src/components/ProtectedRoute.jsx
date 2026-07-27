import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Layout from "./Layout";

// 로그인 안 한 상태로 /scanner, /chatbot, /menu 같은 페이지에 직접 들어오려 하면
// /login으로 강제로 돌려보냄 (원래 Streamlit의 로그인 체크 로직과 같은 목적)
export default function ProtectedRoute({ children }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <Layout>{children}</Layout>;
}
