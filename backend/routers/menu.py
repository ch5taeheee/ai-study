import ollama
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# 프론트에서 보내는 기분/카테고리/위치 값의 형태
class MenuRequest(BaseModel):
    mood: str
    category: str
    location: str


# 사용자 상황(기분/선호/위치)을 프롬프트에 채워서 LLM한테 메뉴 하나 추천받기
@router.post("/recommend")
def recommend(payload: MenuRequest):
    prompt = f"""
    당신은 메뉴를 추천하는 담당자입니다. 사용자의 상황에 맞게
    한 가지의 메뉴와 이유를 추천해주세요.

    [상황]
    기분 : {payload.mood}
    선호카테고리 : {payload.category}
    위치 : {payload.location}

    [양식]
    추천 메뉴 :
    추천 이유 :
    """

    response = ollama.generate(model="gemma2:2b", prompt=prompt)
    return {"result": response["response"]}
