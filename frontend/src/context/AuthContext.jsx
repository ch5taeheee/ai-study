import { createContext, useContext, useState } from "react";

// 로그인한 사용자 정보를 앱 전체 어디서나 꺼내 쓸 수 있게 해주는 통로
// (Streamlit의 st.session_state['user_info']와 같은 역할)
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  // 새로고침해도 로그인이 풀리지 않도록 localStorage에서 먼저 복원 시도
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user");
    return saved ? JSON.parse(saved) : null;
  });

  const login = (userInfo) => {
    setUser(userInfo);
    localStorage.setItem("user", JSON.stringify(userInfo));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// 다른 컴포넌트에서 const { user, login, logout } = useAuth(); 형태로 사용
export function useAuth() {
  return useContext(AuthContext);
}
