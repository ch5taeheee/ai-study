import { useState } from "react";
import api from "../api";

export default function SmartScanner() {
  const [preview, setPreview] = useState(null); // 업로드한 이미지 미리보기용 URL
  const [rawText, setRawText] = useState("");   // OCR이 읽어낸 원본 텍스트
  const [fields, setFields] = useState(null);   // LLM이 정리해준 필드(회사명/이름 등)
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 파일 선택하자마자 바로 업로드 -> OCR -> LLM 순서로 진행 (버튼 따로 없음)
  const handleFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file)); // 브라우저에서 로컬 미리보기 (서버 왕복 없이 즉시 표시)
    setFields(null);
    setRawText("");
    setError("");
    setLoading(true);

    // 파일은 JSON이 아니라 FormData(multipart)로 보내야 FastAPI의 UploadFile이 받을 수 있음
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/scanner/scan", formData);
      setRawText(res.data.raw_text);
      if (res.data.error) {
        setError(res.data.error);
      } else {
        setFields(res.data.fields);
      }
    } catch (err) {
      setError("스캔 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>📇 AI 스마트 명함 관리</h2>
      <p>이 앱은 Ollama(로컬 LLM)를 사용하여 데이터를 로컬에서 분석합니다.</p>

      <input type="file" accept="image/jpeg,image/png" onChange={handleFile} />

      {preview && (
        <div style={{ marginTop: 16 }}>
          <img src={preview} alt="업로드된 명함" width={400} />
        </div>
      )}

      {loading && <p>⏳ OCR + AI 분석 중...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {rawText && (
        <div style={{ marginTop: 16 }}>
          <strong>OCR 원문</strong>
          <p>{rawText}</p>
        </div>
      )}

      {/* LLM이 뽑아준 값들을 수정 가능한 입력창에 채워서 보여줌 (원래 Streamlit 버전과 동일한 UX) */}
      {fields && (
        <div style={{ marginTop: 16, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, maxWidth: 600 }}>
          <label>
            🏢 회사명
            <input defaultValue={fields.company_name} />
          </label>
          <label>
            📞 전화번호
            <input defaultValue={fields.phone} />
          </label>
          <label>
            👤 이름
            <input defaultValue={fields.name} />
          </label>
          <label>
            📧 이메일
            <input defaultValue={fields.email} />
          </label>
          <label>
            🏷️ 직급
            <input defaultValue={fields.position} />
          </label>
        </div>
      )}
    </div>
  );
}
