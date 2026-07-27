from itertools import combinations

import numpy as np
import ollama
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class SimilarityRequest(BaseModel):
    sentences: list[str]


# 문장 하나를 768차원 벡터로 변환 (Day1 학습 내용)
def embed(text: str) -> np.ndarray:
    res = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return np.array(res["embedding"])


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


# Day1: 문장 여러 개를 받아서 모든 쌍의 코사인 유사도를 계산해 반환
@router.post("/day1/similarity")
def day1_similarity(payload: SimilarityRequest):
    sentences = [s for s in payload.sentences if s.strip()]
    embeddings = [embed(s) for s in sentences]

    pairs = []
    for (i, s1), (j, s2) in combinations(enumerate(sentences), 2):
        score = cosine_similarity(embeddings[i], embeddings[j])
        pairs.append({"a": s1, "b": s2, "score": round(score, 4)})

    pairs.sort(key=lambda p: p["score"], reverse=True)
    return {"dimension": len(embeddings[0]) if embeddings else 0, "pairs": pairs}
