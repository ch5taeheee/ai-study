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

  useEffect(() => {
    api.get("/auth/companies").then((res) => setCompanies(res.data.companies));
  }, []);

  const isReady = companyName && employeeId && employeeName;

  const handleLogin = async () => {
    setError("");
    try {
      const res = await api.post("/auth/login", {
        company_name: companyName,
        employee_id: employeeId,
        employee_name: employeeName,
      });
      login(res.data);
      navigate("/chatbot");
    } catch (err) {
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
