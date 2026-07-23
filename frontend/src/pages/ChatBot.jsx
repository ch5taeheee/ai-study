import { useState } from "react";
import api from "../api";

export default function ChatBot() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const isReady = file && question.trim() !== "";

  const handleAsk = async () => {
    setLoading(true);
    setAnswer("");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("question", question);

    try {
      const res = await api.post("/chatbot/ask", formData);
      setAnswer(res.data.answer);
    } catch {
      setAnswer("에러가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>📑 내 연차는 얼마? PDF 문서 챗봇</h2>
      <p>규정집 PDF를 올리고 궁금한 점을 물어보세요.</p>

      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />

      {file && (
        <>
          <br />
          <br />
          <input
            style={{ width: 400 }}
            placeholder="질문을 입력하세요 (예: 내 연차는 며칠이야?)"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <br />
          <br />
          <button disabled={!isReady || loading} onClick={handleAsk}>
            AI에게 물어보기
          </button>
        </>
      )}

      {loading && <p>⏳ 답변 생성 중...</p>}
      {answer && (
        <div style={{ marginTop: 16 }}>
          <strong>🤖 답변</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
