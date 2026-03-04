import streamlit as st
import pandas as pd

# 1. 텍스트 요소들
st.title("이것은 제목입니다 (Title)")
st.header("이것은 헤더입니다 (Header)")
st.subheader("이것은 서브헤더입니다 (Subheader)")
st.write("일반적인 텍스트나 데이터프레임, 객체를 출력할 때 씁니다.")

st.divider() # 구분선

# 2. 입력 위젯들
st.header("입력 위젯 모음")

name = st.text_input("이름을 입력하세요", placeholder="홍길동")
age = st.number_input("나이를 입력하세요", min_value=0, max_value=120, value=25)

status = st.radio("오늘의 기분은?", ("좋음", "보통", "나쁨"))

if st.button("확인 버튼"):
    st.success(f"{name}({age})님, 기분이 '{status}'이시군요!")

# 3. 데이터 출력 (표, 차트)
st.divider()
st.header("데이터 출력")

data = {
    '이름': ['A', 'B', 'C'],
    '점수': [80, 95, 70]
}
df = pd.DataFrame(data)

st.table(df) # 정적인 표
st.line_chart(df['점수']) # 간단한 라인 차트

# 4. 사이드바
with st.sidebar:
    st.header("사이드바 메뉴")
    st.selectbox("옵션 선택", ["옵션 1", "옵션 2", "옵션 3"])