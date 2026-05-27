import streamlit as st
import google.generativeai as genai

# Secrets에서 API 키 불러오기
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

st.title("🤖 간단 챗봇")
st.caption("제미나이로 만든 질문-답변 앱")

# 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 입력 받기
if prompt := st.chat_input("궁금한 걸 물어보세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"오류가 발생했어요: {e}")
