import streamlit as st
import pdfplumber
import ollama
import pandas as pd
from Utils import  navigate_to
from apps.base.ChatBot import chatbot

def appLogin():
    print(st.session_state)
    if st.session_state.get('authenticated'):
        chatbot()
        st.stop()

    # # --- 페이지 이동
    # if 'auth_message' in st.session_state:
    #     if st.session_state['authenticated']:
    #        navigate_to("ChatBot")
    #     else:
    #         st.error(st.session_state['auth_message'])

    # --- csv 파일
    memberData = pd.read_csv('common/members.csv')
    member_list = memberData.to_dict('records')
    # --- csv 파일

    # --- 사이드바 설정

    # --- 사이드바 설정

    def handle_login(data):
        # (디버깅용) 터미널 콘솔창에는 찍힙니다.
        # print(f"함수 내부에서 받은 데이터: {data[0]}")
        input_company = data[0]
        input_id = str(data[1]).strip() # 문자열로 변환 및 공백 제거
        input_name = data[2].strip()

        matched_user = memberData[
            (memberData['company_name'] == input_company) & 
            (memberData['employee_id'].astype(str) == input_id) & 
            (memberData['employee_name'] == input_name)
        ]

        print("유저정보",matched_user)

        # 2. 결과 확인
        if not matched_user.empty:
            print(" 성공")
            # 일치하는 데이터가 있음 -> 로그인 성공
        
            st.session_state['authenticated'] = True
            st.session_state['user_info'] = matched_user.iloc[0].to_dict() # 해당 유저 정보 저장
            # st.session_state['auth_message'] = f"✅ {input_name}님, 인증되었습니다."
            st.session_state['current_page'] = "ChatBot"
            navigate_to('ChatBot')
            print('이동')
        else:
            # 일치하는 데이터가 없음 -> 로그인 실패
            st.session_state['authenticated'] = False
            st.session_state['auth_message'] = "❌ 일치하는 정보가 없습니다. 다시 입력해주세요."
            print("실패")
        

    # --- 스트림릿 UI 시작 ---
    st.set_page_config(page_title="회사인증", page_icon="📑")
    st.title("📑 본인인증")
    st.markdown("본인인증 후 다양한 항목을 이용해보세요")


    #st.write(memberData.company_name)
    if member_list:
        companyList= memberData.company_name # 회사 목록 추출
        companyNm = st.selectbox("Company Name",companyList)

    col1,col2 = st.columns(2)
    with col1:
        employeeId = st.text_input("사번")
    with col2:
        employeeNm = st.text_input("이름")
        
    is_ready = all([companyNm, employeeId, employeeNm])
    col1, col2 = st.columns([4, 1])
    with col1:
        pass

    with col2:
        userData = [companyNm,employeeId,employeeNm]
        st.button("Login", use_container_width=True, disabled=is_ready, on_click=handle_login, args=(userData,))
            

