import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌"
)

st.title("💌 Gemini 연애상담 챗봇")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("API 키를 불러올 수 없습니다.")
    st.stop()

# 모델 설정
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 채팅 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("고민을 입력해보세요...")

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):

        try:
            # 대화 기록 구성
            history_text = ""

            for msg in st.session_state.messages:
                role = "사용자" if msg["role"] == "user" else "상담사"
                history_text += f"{role}: {msg['content']}\n"

            prompt = f"""
            너는 따뜻하고 공감 능력이 뛰어난 연애 상담 챗봇이다.
            연애, 인간관계, 고민 상담을 친절하게 해줘.
            다른 주제 질문도 자연스럽게 답변해줘.

            대화 기록:
            {history_text}

            상담사:
            """

            response = model.generate_content(prompt)

            bot_reply = response.text

            st.markdown(bot_reply)

            # AI 메시지 저장
            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_reply
            })

        except Exception as e:
            error_message = f"오류가 발생했습니다 😢\n\n{e}"

            st.error(error_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })
