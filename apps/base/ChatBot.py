import streamlit as st
import pdfplumber
import ollama
from Utils import show_user_sidebar



def chatbot():
    show_user_sidebar("")
    
    # 1. PDF에서 텍스트를 뽑아내는 함수
    def extract_pdf_text(pdf_file):
        with pdfplumber.open(pdf_file) as pdf:
            full_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        return full_text

    # 2. AI에게 질문하고 답변 받는 함수
    def ask_ai_about_pdf(pdf_text, user_question):
        prompt = f"""
        너는 회사의 인사팀 전문가야. 아래 제공된 [사내 규정 문서]의 내용을 바탕으로 사용자의 질문에 친절하게 답해줘.
        문서에 없는 내용은 "해당 내용은 문서에 명시되어 있지 않습니다"라고 답변해줘.

        [사내 규정 문서]
        {pdf_text}

        [사용자 질문]
        {user_question}
        """
        
        try:
            response = ollama.generate(model='gemma2:2b', prompt=prompt)
            return response['response']
        except Exception as e:
            return f"에러가 발생했습니다: {str(e)}"

    # --- 스트림릿 UI 시작 ---
    st.set_page_config(page_title="사내 규정 AI 조력자", page_icon="📑")
    st.title("📑 내 연차는 얼마? PDF 문서 챗봇")
    st.markdown("규정집 PDF를 올리고 궁금한 점을 물어보세요.")

    # 파일 업로드 섹션
    pdf_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")

    if pdf_file:
        # PDF 텍스트 추출 (캐싱을 통해 속도 향상 가능하지만 여기선 단순하게 구현)
        with st.spinner("문서를 읽고 분석하는 중입니다..."):
            pdf_content = extract_pdf_text(pdf_file)
        
        st.success("✅ 문서 분석 완료!")
        st.divider()

        # 질문 입력창
        user_input = st.text_input("질문을 입력하세요 (예: 내 연차는 며칠이야?, 경조사 휴가는 어떻게 돼?)")

        is_ready = (pdf_file is not None) and (user_input.strip() != "")
        if st.button("AI에게 물어보기", disabled=not is_ready):
            with st.spinner("답변 생성 중..."):
                answer = ask_ai_about_pdf(pdf_content, user_input)
                
                st.chat_message("assistant").write(answer)
        else:
            st.warning("질문을 입력해 주세요!")

    else:
        st.info("먼저 PDF 문서를 업로드해 주세요.")