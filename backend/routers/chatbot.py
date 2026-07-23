import io

import ollama
import pdfplumber
from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


def extract_pdf_text(pdf_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text


@router.post("/ask")
async def ask(file: UploadFile = File(...), question: str = Form(...)):
    pdf_bytes = await file.read()
    pdf_text = extract_pdf_text(pdf_bytes)

    prompt = f"""
    너는 회사의 인사팀 전문가야. 아래 제공된 [사내 규정 문서]의 내용을 바탕으로 사용자의 질문에 친절하게 답해줘.
    문서에 없는 내용은 "해당 내용은 문서에 명시되어 있지 않습니다"라고 답변해줘.

    [사내 규정 문서]
    {pdf_text}

    [사용자 질문]
    {question}
    """

    response = ollama.generate(model="gemma2:2b", prompt=prompt)
    return {"answer": response["response"]}
