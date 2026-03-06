import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import ollama  # Ollama 라이브러리 추가
import json
import re

# 1. 페이지 설정
st.set_page_config(page_title="메뉴 추천 봇", layout="wide")

#프롬프트 설계
def get_ai_menu(user_data):
    st.write(user_data[0])
    st.write(user_data[1])
    st.write(user_data[2])

    prompt = f"""
    당신은 메뉴를 추천하는 담당자입니다. 사용자의 상황에 맞게
    한 가지의 메뉴와 이유를 추천해주세요.

    [상황]
    기분 : {user_data[0]}
    선호카테고리 : {user_data[1]}
    위치 : {user_data[2]}

    [양식]
    추천 메뉴 : 
    추천 이유 :
    """

    response = ollama.generate(
        model ='gemma2:2b', 
        prompt=prompt
    )
    
    return response['response']

st.title("메뉴 추천 봇")

#사용자 입력창
col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("기분", ["좋음","나쁨","신남","우울함","짜증남","슬픔"], index=None, placeholder="당신의 기분은?")
    locate = st.selectbox("위치", ["서울","대전","부산","대구","경기도"], index=None, placeholder="당신의 위치는?")
with col2:
    category = st.selectbox("카테고리",["한식","중식","일식"], index=None, placeholder="선호하는 메뉴는?")

# 2. 모든 값이 비어있지(None이 아닐 때)만 버튼 활성화
user_data = [mood, locate, category]
is_ready = all(user_data)

if st.button("오늘의 메뉴 추천받기", disabled=not is_ready):
    with st.spinner(f"AI가 {user_data[0]} 기분과 {user_data[1]} 위치에 맞춰 메뉴를 고르고 있어요!"):
        result = get_ai_menu(user_data)
    
        # 1. 결과가 정상적으로 있는지 체크
        if result: 
            st.divider()
            st.subheader("🎉 오늘의 점심 추천 결과")
            st.markdown(result)
            st.balloons() # 결과가 있을 때만 축하 풍선!
        
        # 2. 결과가 비어있거나 에러가 났을 경우
        else:
            st.error("AI로부터 응답을 받지 못했습니다. Ollama가 켜져 있는지 확인해 주세요.")
            st.button("다시 시도하기") # 새로고침 유도
else:
    st.caption("💡 모든 항목을 고르시면 추천 버튼이 활성화됩니다.")