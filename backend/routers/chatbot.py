import io

import ollama
import pdfplumber
from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter()


# 업로드된 PDF 파일(bytes)에서 페이지별 텍스트를 뽑아 하나로 합침
def extract_pdf_text(pdf_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text


# PDF 파일 + 질문을 같이 받아서, PDF 내용을 근거로 LLM이 답변하게 함
# File과 Form을 같이 쓰면 파일 업로드 + 일반 텍스트 필드를 한 번에 받을 수 있음 (multipart/form-data)
@router.post("/ask")
async def ask(file: UploadFile = File(...), question: str = Form(...)):
    pdf_bytes = await file.read()
    pdf_text = extract_pdf_text(pdf_bytes)

    # 문서에 없는 내용은 지어내지 말라고 프롬프트에 명시 (환각 방지)
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
