
import streamlit as st
from google import genai

st.set_page_config(
    page_title="마음쉼터",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 마음쉼터")
st.caption("오늘도 수고했어요. 잠시 마음을 쉬어가세요.")

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 사이드바
with st.sidebar:
    st.header("💚 나의 마음 체크")

    stress = st.slider(
        "현재 스트레스는 어느 정도인가요?",
        min_value=0,
        max_value=10,
        value=5
    )

    if stress <= 3:
        st.success("😊 마음이 비교적 편안하네요!")
        st.write("좋은 기분을 유지하며 가볍게 산책해 보세요.")
    elif stress <= 6:
        st.warning("😐 조금 지쳐 있는 것 같아요.")
        st.write("잠깐 쉬면서 좋아하는 음악을 들어보세요.")
    else:
        st.error("😢 스트레스가 높은 상태네요.")
        st.write("잠시 쉬고, 믿을 수 있는 사람과 이야기를 나눠보세요.")

    st.divider()

    st.subheader("🫁 마음 진정 호흡법")
    st.write("1. 4초 동안 천천히 숨 들이마시기")
    st.write("2. 4초 동안 숨 멈추기")
    st.write("3. 6초 동안 천천히 숨 내쉬기")
    st.info("편안한 속도로 3번 반복해 보세요.")

    st.divider()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# AI 챗봇 화면
st.subheader("💬 AI 마음 상담")

st.write("지금 어떤 일이 마음을 힘들게 하나요? 편하게 이야기해 주세요.")

# 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 입력
user_input = st.chat_input("오늘 있었던 일이나 고민을 이야기해 주세요.")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")

            if not api_key:
                st.error("GEMINI_API_KEY가 설정되지 않았습니다.")
            else:
                client = genai.Client(api_key=api_key)

                system_prompt = """
                당신은 따뜻하고 친절한 스트레스 관리 AI 상담 도우미입니다.

                규칙:
                1. 사용자의 감정을 먼저 공감해 주세요.
                2. 비난하거나 판단하지 마세요.
                3. 답변은 한국어로 쉽고 간결하게 작성하세요.
                4. 실천 가능한 스트레스 관리 방법을 1~2개 제안하세요.
                5. 지나치게 긴 답변은 피하세요.
                6. 정신질환을 진단하거나 약물을 권하지 마세요.
                7. 위험하거나 위급한 상황에서는 즉시 주변의
                   신뢰할 수 있는 사람이나 전문기관에
                   도움을 요청하도록 안내하세요.
                8. 자해나 자살 위험이 표현되면 안전을 우선하고,
                   한국의 긴급전화 119 또는 자살예방상담전화
                   109 등의 도움을 안내하세요.
                """

                history = [
                    {
                        "role": (
                            "model" if msg["role"] == "assistant"
                            else "user"
                        ),
                        "parts": [{"text": msg["content"]}]
                    }
                    for msg in st.session_state.messages
                ]

                with st.spinner("마음을 담아 답변하는 중..."):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=history,
                        config={
                            "system_instruction": system_prompt,
                            "temperature": 0.7
                        }
                    )

                answer = response.text

                if not answer:
                    answer = "답변을 만들지 못했어요. 다시 이야기해 주세요."

                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

        except Exception:
            st.error(
                "AI 연결에 문제가 발생했어요. "
                "API 키와 사용 한도를 확인한 뒤 다시 시도해 주세요."
            )

st.divider()
st.caption(
    "🌱 마음쉼터는 전문 심리상담이나 의료 서비스를 "
    "대체하지 않습니다. 대화 내용은 현재 세션에서만 유지됩니다."
)
