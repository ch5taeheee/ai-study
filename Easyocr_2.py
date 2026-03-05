import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import ollama  # Ollama 라이브러리 추가
import json
import re

# 1. 페이지 설정
st.set_page_config(page_title="로컬 AI 명함 스캐너", layout="wide")

# --- 공통 함수: OCR 리더기 캐싱 ---
@st.cache_resource
def load_reader():
    return easyocr.Reader(['ko', 'en'])

def extract_info_with_ollama(raw_text):
    st.write(raw_text)
    """
    사진에서 보여준 프롬프트 형식을 사용하여 Ollama(Llama 3.1)로 분석
    """
    prompt = f"""
    다음은 명함을 스캔한 텍스트입니다. 텍스트에서 정보를 추출해주세요.
    이름, 회사명, 직급, 전화번호, 이메일을 찾아서 아래 양식에 맞게 값만 적어주세요.
    마크다운 기호 없이 ':' 뒤에 값만 적어주세요.
    못 찾겠으면 '없음'이라고 적으세요.

    [텍스트]
    {raw_text}

    [양식]
    회사명:
    이름:
    직급:
    전화번호:
    이메일:
    비고:
    """
    
    try:
        # Ollama 실행 (llama3.1 모델이 미리 'ollama pull llama3.1' 되어 있어야 함)
        response = ollama.generate(
            #model='llama3:latest',
            model = 'gemma2:2b',
            prompt=prompt,
            options={'temperature': 0}
        )
        return response['response']
    except Exception as e:
        return f"에러 발생: {str(e)}\n(Ollama가 실행 중인지 확인하세요)"

# --- UI 부분 ---
st.title("📇AI 스마트 명함 관리")
st.info("이 앱은 Ollama(Llama 3.1)를 사용하여 데이터를 로컬에서 분석합니다.")

reader = load_reader()

uploaded_file = st.file_uploader("명함 이미지를 선택하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='업로드된 명함 사진', width=400)
    
    with st.spinner('1단계: EasyOCR로 글자 읽는 중...'):
        img_array = np.array(image)
        results = reader.readtext(img_array)
        all_text = " ".join([res[1].strip() for res in results])

    if all_text:
        with st.spinner('2단계: 로컬 AI(Llama 3.1)가 분류 중...'):
            ai_result = extract_info_with_ollama(all_text)

        st.divider()
        st.subheader("📝 AI 분석 결과")
        st.write("결과 :" , ai_result)
        
        # AI가 준 텍스트 결과를 딕셔너리로 변환 (한 줄씩 읽어서 분리)
        parsed_data = {}
        for line in ai_result.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                parsed_data[key.strip()] = value.strip()

        # 결과 입력창에 자동 채우기
        col1, col2 = st.columns(2)
        with col1:
            final_company = st.text_input("🏢 회사명", value=parsed_data.get("회사명", ""))
            final_name = st.text_input("👤 이름", value=parsed_data.get("이름", ""))
            final_job = st.text_input("🏷️ 직급", value=parsed_data.get("직급", ""))
        
        with col2:
            final_phone = st.text_input("📞 전화번호", value=parsed_data.get("전화번호", ""))
            final_email = st.text_input("📧 이메일", value=parsed_data.get("이메일", ""))
            final_birth = st.text_input("🎂 생일", placeholder="YYYY-MM-DD")

        if st.button("💾 정보 저장하기"):
            st.success(f"'{final_name}'님의 정보가 로컬에 준비되었습니다.")
            st.json(parsed_data)
    else:
        st.error("텍스트를 인식하지 못했습니다.")
