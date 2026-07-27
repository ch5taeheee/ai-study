import json

import easyocr
import numpy as np
import ollama
from fastapi import APIRouter, File, UploadFile
from PIL import Image
import io

router = APIRouter()

# easyocr.Reader 로딩이 느려서 서버 시작할 때 한 번만 만들고 계속 재사용
# (Streamlit의 @st.cache_resource랑 같은 목적)
_reader = None


def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["ko", "en"])
    return _reader


# OCR로 뽑은 텍스트를 로컬 LLM(Ollama)에게 보내서 명함 필드만 추출
# format="json"으로 강제해서 항상 파싱 가능한 형태로 응답받음
# (예전 방식: ":" 기준으로 문자열 split -> 모델이 형식을 조금만 벗어나도 깨짐)
def extract_info_with_ollama(raw_text: str) -> dict:
    prompt = f"""
    다음은 명함을 스캔한 텍스트입니다. 텍스트에서 정보를 추출해서 JSON으로만 답해주세요.
    키는 company_name, name, position, phone, email 입니다.
    못 찾은 값은 빈 문자열로 두세요.

    [텍스트]
    {raw_text}
    """

    response = ollama.generate(
        model="gemma2:2b",
        prompt=prompt,
        format="json",
        options={"temperature": 0},  # 0으로 두면 매번 같은 입력에 같은 결과 (창의성 X, 일관성 우선)
    )

    try:
        return json.loads(response["response"])
    except json.JSONDecodeError:
        # 그래도 모델이 이상한 응답을 줄 수 있으니 최후의 방어선으로 빈 값 반환
        return {"company_name": "", "name": "", "position": "", "phone": "", "email": ""}


# 프론트에서 이미지 파일을 업로드하면: OCR로 글자 읽기 -> LLM으로 필드 추출 -> JSON 응답
@router.post("/scan")
async def scan_card(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    reader = get_reader()
    results = reader.readtext(np.array(image))
    raw_text = " ".join(res[1].strip() for res in results)  # 인식된 텍스트 조각들을 한 줄로 합침

    if not raw_text:
        return {"raw_text": "", "fields": None, "error": "텍스트를 인식하지 못했습니다."}

    fields = extract_info_with_ollama(raw_text)
    return {"raw_text": raw_text, "fields": fields, "error": None}
