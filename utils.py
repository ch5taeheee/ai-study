import streamlit as st



def show_user_sidebar(data):
    """모든 페이지에서 공통으로 사용할 사이드바 회원 정보 함수"""
    if data is not None and data !='main':
        # --- 1. 로그인 체크
        if st.session_state: 
            if 'authenticated' in st.session_state:
                st.success("성공")
            else:
                st.warning("로그인이 필요한 서비스입니다.")
        else:
            st.warning("로그인이 필요한 서비스입니다.")
            st.switch_page("Main.py")

        # --- 핵심: 자동 생성된 사이드바 메뉴 숨기기 ---
        st.set_page_config(initial_sidebar_state="expanded") # 사이드바 열림 유지
        
        # --- 2. 사이드바 구성
        with st.sidebar:
            st.header("👤 내 정보")
            # 세션에 저장된 유저 정보 가져오기
            user = st.session_state.get('user_info',{})
            st.write(f"🏢 **소속**: {user.get('company_name', '-')}")
            st.write(f"📂 **부서**: {user.get('dept_name', '-')}")
            st.write(f"🆔 **사번**: {user.get('employee_id', '-')}")
            st.divider()

            # --- 3. 메뉴 이동 버튼
            st.markdown("dd")
            menu_items = {
                "ChatBot.py": "🤖 AI 규정 챗봇",
                "MenuBot.py": "🍴 오늘 뭐 먹지?",
                "SmartScanner.py": "📸 스마트 스캐너"
            }

            for file_name, menu_name in menu_items.items():
                # key값은 중복 방지를 위해 파일명을 활용합니다.
                if st.button(menu_name, key=f"btn_{file_name}", use_container_width=True):
                    st.switch_page(f"apps/base/{file_name}")

            st.divider()

            if st.button("🔒 로그아웃", key="logout_btn", use_container_width=True):
                st.session_state.clear()
                st.switch_page("Main.py")
            #
   
# --- 다른 페이지로 이동하는 함수
def navigate_to(page, params=None):
    print('여기22')
    print(st.session_state)
    print(page)
    print("------------------------------------")

    if params:
        st.session_state['page_params'] = params
    else:
        st.session_state['page_params'] = {}

    st.session_state['current_page'] = page
    
    st.rerun()