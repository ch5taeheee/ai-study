import { useState } from "react";
import api from "../api";

// 앞으로 Day가 늘어날 때마다 여기에 항목만 추가하면 됨
const DAYS = [
  { id: "day1", label: "Day1: 임베딩 이해" },
  { id: "day2", label: "Day2: 문서 전처리 & 청킹 (준비중)" },
  { id: "day3", label: "Day3: 벡터DB 세팅 (준비중)" },
];

// Day1: 문장 여러 개를 입력하면 임베딩 후 코사인 유사도를 계산해서 보여줌
function Day1Similarity() {
  const [sentences, setSentences] = useState(["", "", "", ""]);
  const [dimension, setDimension] = useState(null);
  const [pairs, setPairs] = useState([]);
  const [loading, setLoading] = useState(false);

  const updateSentence = (idx, value) => {
    const next = [...sentences];
    next[idx] = value;
    setSentences(next);
  };

  const handleCalculate = async () => {
    const filled = sentences.filter((s) => s.trim() !== "");
    if (filled.length < 2) return;

    setLoading(true);
    setPairs([]);
    try {
      const res = await api.post("/test/day1/similarity", { sentences: filled });
      setDimension(res.data.dimension);
      setPairs(res.data.pairs);
    } catch {
      setDimension(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>임베딩 & 코사인 유사도</h3>
      <p>문장을 2~4개 입력하고 유사도를 계산해보세요. (의미가 비슷한 문장끼리 값이 높게 나오는지 확인)</p>

      {sentences.map((s, idx) => (
        <div key={idx} style={{ marginBottom: 8 }}>
          <input
            style={{ width: 400 }}
            placeholder={`문장 ${idx + 1}`}
            value={s}
            onChange={(e) => updateSentence(idx, e.target.value)}
          />
        </div>
      ))}

      <button onClick={handleCalculate} disabled={loading}>
        {loading ? "계산 중..." : "유사도 계산"}
      </button>

      {dimension !== null && <p style={{ marginTop: 12 }}>벡터 차원 수: {dimension}</p>}

      {pairs.length > 0 && (
        <table style={{ marginTop: 12, borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ border: "1px solid #ddd", padding: 6 }}>유사도</th>
              <th style={{ border: "1px solid #ddd", padding: 6 }}>문장 A</th>
              <th style={{ border: "1px solid #ddd", padding: 6 }}>문장 B</th>
            </tr>
          </thead>
          <tbody>
            {pairs.map((p, idx) => (
              <tr key={idx}>
                <td style={{ border: "1px solid #ddd", padding: 6 }}>{p.score}</td>
                <td style={{ border: "1px solid #ddd", padding: 6 }}>{p.a}</td>
                <td style={{ border: "1px solid #ddd", padding: 6 }}>{p.b}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default function TestLab() {
  const [activeDay, setActiveDay] = useState("day1");

  return (
    <div>
      <h2>🧪 TEST 실습실</h2>

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        {DAYS.map((d) => (
          <button
            key={d.id}
            onClick={() => setActiveDay(d.id)}
            style={{ fontWeight: activeDay === d.id ? "bold" : "normal" }}
          >
            {d.label}
          </button>
        ))}
      </div>
      <hr />

      {activeDay === "day1" && <Day1Similarity />}
      {activeDay !== "day1" && <p>준비 중입니다.</p>}
    </div>
  );
}
