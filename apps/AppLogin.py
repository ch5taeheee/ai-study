import streamlit as st
import pandas as pd
from Utils import navigate_to

def appLogin():
    if st.session_state.get('authenticated'):
        navigate_to('chatBot')
        return

    st.title("📑 본인인증")
    st.markdown("본인인증 후 서비스를 이용해주세요.")

    # 데이터 로드 (경로 주의)
    try:
        memberData = pd.read_csv('common/members.csv')
        companyList = memberData['company_name'].unique()
    except:
        st.error("회원 정보를 불러올 수 없습니다.")
        return

    companyNm = st.selectbox("Company Name", companyList)
    col1, col2 = st.columns(2)
    with col1:
        employeeId = st.text_input("사번")
    with col2:
        employeeNm = st.text_input("이름")

    is_not_ready = not (companyNm and employeeId and employeeNm)

    def handle_login():
        input_id = str(employeeId).strip()
        matched_user = memberData[
            (memberData['company_name'] == companyNm) & 
            (memberData['employee_id'].astype(str) == input_id) & 
            (memberData['employee_name'] == employeeNm.strip())
        ]

        if not matched_user.empty:
            st.session_state['authenticated'] = True
            st.session_state['user_info'] = matched_user.iloc[0].to_dict()
            # navigate_to('chatBot')
            st.switch_page("pages/ChatBot.py")
        else:
            st.error("❌ 일치하는 정보가 없습니다.")

    st.button("Login", use_container_width=True, 
              disabled=is_not_ready, 
              on_click=handle_login)