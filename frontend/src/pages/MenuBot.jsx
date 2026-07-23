import { useState } from "react";
import api from "../api";

const MOODS = ["좋음", "나쁨", "신남", "우울함", "짜증남", "슬픔"];
const CATEGORIES = ["한식", "중식", "일식"];
const LOCATIONS = ["서울", "대전", "부산", "대구", "경기도"];

export default function MenuBot() {
  const [mood, setMood] = useState("");
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const isReady = mood && category && location;

  const handleRecommend = async () => {
    setLoading(true);
    setResult("");
    try {
      const res = await api.post("/menu/recommend", { mood, category, location });
      setResult(res.data.result);
    } catch {
      setResult("AI로부터 응답을 받지 못했습니다. Ollama가 켜져 있는지 확인해 주세요.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>메뉴 추천 봇</h2>

      <select value={mood} onChange={(e) => setMood(e.target.value)}>
        <option value="">당신의 기분은?</option>
        {MOODS.map((m) => (
          <option key={m} value={m}>{m}</option>
        ))}
      </select>

      <select value={location} onChange={(e) => setLocation(e.target.value)} style={{ marginLeft: 8 }}>
        <option value="">당신의 위치는?</option>
        {LOCATIONS.map((l) => (
          <option key={l} value={l}>{l}</option>
        ))}
      </select>

      <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ marginLeft: 8 }}>
        <option value="">선호하는 메뉴는?</option>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>{c}</option>
        ))}
      </select>

      <br />
      <br />
      <button disabled={!isReady || loading} onClick={handleRecommend}>
        오늘의 메뉴 추천받기
      </button>

      {loading && <p>⏳ AI가 메뉴를 고르고 있어요!</p>}
      {result && (
        <div style={{ marginTop: 16 }}>
          <h3>🎉 오늘의 점심 추천 결과</h3>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}
