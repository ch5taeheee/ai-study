import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const MENU_ITEMS = [
  { path: "/chatbot", label: "🤖 AI 규정 챗봇" },
  { path: "/menu", label: "🍴 오늘 뭐 먹지?" },
  { path: "/scanner", label: "📸 스마트 스캐너" },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside style={{ width: 240, borderRight: "1px solid #ddd", padding: 16 }}>
        <h3>👤 내 정보</h3>
        <p>🏢 소속: {user?.company_name ?? "-"}</p>
        <p>📂 부서: {user?.dept_name ?? "-"}</p>
        <p>🆔 사번: {user?.employee_id ?? "-"}</p>
        <hr />
        {MENU_ITEMS.map((item) => (
          <div key={item.path} style={{ marginBottom: 8 }}>
            <Link to={item.path}>{item.label}</Link>
          </div>
        ))}
        <hr />
        <button onClick={handleLogout}>🔒 로그아웃</button>
      </aside>
      <main style={{ flex: 1, padding: 24 }}>{children}</main>
    </div>
  );
}
