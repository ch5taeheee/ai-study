import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="AI 멀티 툴", layout="wide")

# 2. 사이드바 메뉴
with st.sidebar:
    st.title("🤖 AI 서비스 선택")
    menu = st.radio(
        "이용하실 서비스를 선택하세요:",
        ("📇 명함 스캐너", "🍱 맛집 추천 AI")
    )
    st.info("메뉴를 선택하면 해당 기능만 표시됩니다.")

# --- 공통 함수: OCR 리더기 ---
@st.cache_resource
def load_reader():
    return easyocr.Reader(['ko', 'en'])

# ==========================================
# 메뉴 1: 명함 스캐너 화면
# ==========================================
if menu == "📇 명함 스캐너":
    st.title("📇 스마트 명함 관리자")
    st.write("명함 사진을 올리면 회사명, 이름, 연락처를 자동으로 분류합니다.")
    
    reader = load_reader()

    # 파일 업로드 (이 블록 안에 있어야 '맛집 추천' 클릭 시 사라집니다)
    uploaded_file = st.file_uploader("명함 이미지를 선택하세요 (JPG, PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='업로드된 명함 사진', width=500)
        
        with st.spinner('AI가 명함 정보를 분석 중입니다...'):
            img_array = np.array(image)
            results = reader.readtext(img_array)

        if results:
            all_text = [res[1].strip() for res in results]
            full_string = " ".join(all_text)

            # 추출 로직
            guessed_company = all_text[0] if len(all_text) > 0 else ""
            guessed_name = all_text[1] if len(all_text) > 1 else (all_text[0] if all_text else "")

            # 직급 키워드
            job_keywords = ['대표', '이사', '부장', '과장', '팀장', '대리', '사원', '주임', '연구원', 'CEO', 'Manager']
            guessed_job = ""
            for text in all_text:
                if any(kw in text for kw in job_keywords):
                    guessed_job = text
                    break
            
            phone_pattern = r'\d{2,3}-\d{3,4}-\d{4}'
            phones = re.findall(phone_pattern, full_string)
            email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            emails = re.findall(email_pattern, full_string)

            st.divider()
            st.subheader("📝 추출 정보 확인")
            col1, col2, col3 = st.columns(3)

            with col1:
                final_company = st.text_input("🏢 회사명", value=guessed_company)
                final_name = st.text_input("👤 이름", value=guessed_name.replace(" ", ""))
            with col2:
                final_job = st.text_input("🏷️ 직급", value=guessed_job)
                final_phone = st.text_input("📞 전화번호", value=phones[0] if phones else "")
            with col3:
                final_email = st.text_input("📧 이메일", value=emails[0] if emails else "")
                final_birth = st.text_input("🎂 생일", placeholder="YYYY-MM-DD")

            if st.button("💾 이 연락처 저장하기"):
                st.success(f"'{final_name}'님의 정보가 준비되었습니다.")
                st.json({"회사": final_company, "이름": final_name, "직급": final_job, "번호": final_phone, "이메일": final_email})

            with st.expander("🔍 원본 텍스트 보기"):
                st.write(all_text)
        else:
            st.error("이미지에서 글자를 인식하지 못했습니다.")

# ==========================================
# 메뉴 2: 맛집 추천 AI 화면
# ==========================================
# elif menu == "🍱 맛집 추천 AI":
#     st.title("🍱 네이버 지도 기반 맛집 추천")
#     st.write("가고 싶은 지역과 메뉴를 입력하면 네이버 지도로 연결해 드려요!")
    
#     # 지역 및 메뉴 입력창
#     col1, col2 = st.columns(2)
#     with col1:
#         location = st.text_input("📍 지역 입력", placeholder="예: 강남역")
#     with col2:
#         food_type = st.text_input("🍕 음식 종류", placeholder="예: 초밥")

#     if st.button("🔍 맛집 검색하기"):
#         if location and food_type:
#             search_query = f"{location} {food_type} 맛집"
#             # 네이버 지도 검색 URL
#             naver_map_url = f"https://map.naver.com/v5/search/{search_query}"
            
#             st.success(f"'{location}' 주변의 '{food_type}' 맛집을 검색합니다.")
#             st.markdown(f'[네이버 지도에서 "{search_query}" 검색 결과 보기]({naver_map_url})')
#         else:
#             st.warning("지역과 음식 종류를 모두 입력해 주세요!")