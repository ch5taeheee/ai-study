import json

import easyocr
import numpy as np
import ollama
from fastapi import APIRouter, File, UploadFile
from PIL import Image
import io

router = APIRouter()

_reader = None


def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["ko", "en"])
    return _reader


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
        options={"temperature": 0},
    )

    try:
        return json.loads(response["response"])
    except json.JSONDecodeError:
        return {"company_name": "", "name": "", "position": "", "phone": "", "email": ""}


@router.post("/scan")
async def scan_card(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    reader = get_reader()
    results = reader.readtext(np.array(image))
    raw_text = " ".join(res[1].strip() for res in results)

    if not raw_text:
        return {"raw_text": "", "fields": None, "error": "텍스트를 인식하지 못했습니다."}

    fields = extract_info_with_ollama(raw_text)
    return {"raw_text": raw_text, "fields": fields, "error": None}
