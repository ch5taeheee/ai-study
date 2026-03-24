import streamlit as st
from apps.AppLogin import appLogin
from Utils import show_user_sidebar, navigate_to

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Main"

if 'page_params' not in st.session_state:
    st.session_state['page_params'] = {}

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False


# 메인 페이지
if st.session_state['current_page'] == "Main":
    show_user_sidebar("main")
    st.title("🏠 메인 페이지")
    st.divider()
    
    if st.button("로그인하러 가기"):
        navigate_to("AppLogin")


# 로그인 페이지
elif st.session_state['current_page'] == "AppLogin":
    appLogin()
    st.stop()