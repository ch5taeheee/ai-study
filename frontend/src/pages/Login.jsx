import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [companies, setCompanies] = useState([]);
  const [companyName, setCompanyName] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [employeeName, setEmployeeName] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  // 화면이 처음 뜰 때 딱 한 번, 회사 목록을 백엔드에서 받아와 드롭다운 채우기
  useEffect(() => {
    api.get("/auth/companies").then((res) => {
      console.log(res)
      setCompanies(res.data.companies);
    });
  }, []);

  // 세 값이 다 채워져야 로그인 버튼 활성화 (원래 Streamlit의 is_not_ready 로직)
  const isReady = companyName && employeeId && employeeName;

  const handleLogin = async () => {
    setError("");
    try {
      const res = await api.post("/auth/login", {
        company_name: companyName,
        employee_id: employeeId,
        employee_name: employeeName,
      });
      login(res.data); // AuthContext에 로그인 정보 저장
      navigate("/chatbot"); // 로그인 성공하면 첫 화면(챗봇)으로 이동
    } catch (err) {
      // 백엔드가 401과 함께 보낸 에러 메시지를 그대로 보여줌
      setError(err.response?.data?.detail ?? "로그인에 실패했습니다.");
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "80px auto" }}>
      <h2>📑 본인인증</h2>
      <p>본인인증 후 서비스를 이용해주세요.</p>

      <select value={companyName} onChange={(e) => setCompanyName(e.target.value)}>
        <option value="">Company Name</option>
        {companies.map((c) => (
          
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>
      <br />
      <br />
      <input
        placeholder="사번"
        value={employeeId}
        onChange={(e) => setEmployeeId(e.target.value)}
      />
      <input
        placeholder="이름"
        value={employeeName}
        onChange={(e) => setEmployeeName(e.target.value)}
        style={{ marginLeft: 8 }}
      />
      <br />
      <br />
      <button disabled={!isReady} onClick={handleLogin} style={{ width: "100%" }}>
        Login
      </button>
      {error && <p style={{ color: "red" }}>❌ {error}</p>}
    </div>
  );
}
