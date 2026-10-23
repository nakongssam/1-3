
import streamlit as st
from google import genai

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="쉬운 지하철 AI 도우미",
    page_icon="🚇",
    layout="centered"
)

# -----------------------------
# 화면 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F8FAF7;
}

.block-container {
    max-width: 760px;
    padding-top: 25px;
    padding-bottom: 70px;
}

h1, h2, h3 {
    color: #1C3324 !important;
}

.hero {
    padding: 20px 0 25px;
}

.hello {
    color: #63B66E;
    font-size: 20px;
    font-weight: 700;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #192A1E;
    margin-top: 12px;
}

.hero-desc {
    color: #738576;
    font-size: 18px;
    line-height: 1.8;
}

.stButton > button {
    background-color: #287E4B !important;
    color: white !important;
    border-radius: 25px !important;
    border: none !important;
    min-height: 48px;
    font-size: 17px !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background-color: #176238 !important;
    color: white !important;
}

div[data-testid="stChatMessage"] {
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 12px;
}

div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background-color: #E6F4E8;
}

div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background-color: #FFFFFF;
}

div[data-testid="stChatMessageContent"] {
    font-size: 19px;
    line-height: 1.8;
}

div[data-testid="stChatInput"] {
    border-radius: 20px;
    border: 2px solid #CFE5D2;
}

.footer {
    text-align: center;
    color: #78947E;
    padding: 25px 0;
    font-size: 14px;
}

@media (max-width: 500px) {
    .hero-title {
        font-size: 29px;
    }
    .block-container {
        padding-left: 14px;
        padding-right: 14px;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# AI 안내 규칙
# -----------------------------
SYSTEM_PROMPT = """
당신은 한국의 어르신을 위한 친절한 지하철 안내 AI입니다.

역할:
1. 서울 및 수도권 지하철 노선 질문에 답합니다.
2. 출발역과 도착역이 있으면 이동 방법을 설명합니다.
3. 몇 호선을 타야 하는지 알려줍니다.
4. 환승이 필요하면 환승역을 알려줍니다.
5. 지하철 용어를 쉬운 한국어로 설명합니다.

답변 규칙:
- 존댓말을 사용하세요.
- 어르신도 이해하기 쉬운 짧은 문장으로 답하세요.
- 중요한 정보는 번호를 붙여 설명하세요.
- 한 번에 너무 많은 정보를 주지 마세요.
- 출발역이나 도착역이 없으면 질문하세요.
- 확실하지 않은 노선 정보는 추측하지 마세요.
- 실제 경로와 운행 정보는 변동될 수 있음을 안내하세요.
- 실시간 열차 위치, 지연, 막차 시간은 확인할 수 없다고
  설명하세요.
- 교통약자 이동 편의시설 정보는 공식 자료 확인을 권하세요.
- 지하철과 관련 없는 질문은 정중하게 안내하세요.
"""

# -----------------------------
# API 키 확인
# -----------------------------
try:
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    API_KEY = ""

# -----------------------------
# 채팅 기록
# -----------------------------
WELCOME = (
    "안녕하세요! 😊\n\n"
    "저는 **쉬운 지하철 AI 도우미**예요.\n\n"
    "어디로 가고 싶으신가요?\n\n"
    "출발역과 도착역을 알려주시면 "
    "쉽게 안내해 드릴게요. 🚇"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME}
    ]

# -----------------------------
# 상단 화면
# -----------------------------
st.markdown("### 🚇 EASY METRO 🌿")

st.markdown("""
<div class="hero">
    <div class="hello">Hello, Traveler! 👋</div>
    <div class="hero-title">
        무엇이 궁금하세요?
    </div>
    <div class="hero-desc">
        복잡한 지하철도 쉽고 편안하게.<br>
        AI 도우미에게 편하게 물어보세요.
    </div>
</div>
""", unsafe_allow_html=True)

st.info(
    "🌱 지하철 노선, 환승 방법, "
    "이용 방법을 질문할 수 있어요."
)

# -----------------------------
# 추천 질문
# -----------------------------
st.markdown("#### 💡 이런 질문을 해보세요")

col1, col2 = st.columns(2)

with col1:
    example1 = st.button(
        "🚉 서울역 → 강남역",
        use_container_width=True
    )

with col2:
    example2 = st.button(
        "🔄 환승이 뭐예요?",
        use_container_width=True
    )

col3, col4 = st.columns(2)

with col3:
    example3 = st.button(
        "🚇 2호선 알려줘",
        use_container_width=True
    )

with col4:
    example4 = st.button(
        "♿ 엘리베이터 이용",
        use_container_width=True
    )

selected_question = None

if example1:
    selected_question = (
        "서울역에서 강남역까지 "
        "지하철로 어떻게 가나요?"
    )
elif example2:
    selected_question = (
        "지하철 환승이 무엇인지 "
        "쉽게 설명해 주세요."
    )
elif example3:
    selected_question = (
        "서울 지하철 2호선에 대해 알려주세요."
    )
elif example4:
    selected_question = (
        "지하철역에서 엘리베이터를 "
        "이용하는 방법을 알려주세요."
    )

st.divider()

# -----------------------------
# 대화 기록 표시
# -----------------------------
st.markdown("### 💬 AI와 대화하기")

for message in st.session_state.messages:
    avatar = (
        "🌿" if message["role"] == "assistant"
        else "👤"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
user_input = st.chat_input(
    "지하철에 대해 질문해 보세요..."
)

prompt = selected_question or user_input

if prompt:

    # 사용자 질문 저장
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🌿"):

        if not API_KEY:
            answer = (
                "⚠️ AI 연결 설정이 필요합니다.\n\n"
                "Streamlit Secrets에 "
                "`GEMINI_API_KEY`를 등록해 주세요."
            )

        else:
            try:
                client = genai.Client(
                    api_key=API_KEY
                )

                # 기존 대화를 텍스트로 전달
                history = []

                for msg in st.session_state.messages[-12:]:
                    role = (
                        "사용자"
                        if msg["role"] == "user"
                        else "도우미"
                    )

                    history.append(
                        f"{role}: {msg['content']}"
                    )

                conversation = "\n\n".join(history)

                with st.spinner(
                    "🌱 지하철 정보를 생각하고 있어요..."
                ):
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=conversation,
                        config={
                            "system_instruction": SYSTEM_PROMPT,
                            "temperature": 0.2
                        }
                    )

                answer = response.text

                if not answer:
                    answer = (
                        "죄송합니다. 답변을 만들지 못했어요. "
                        "다시 질문해 주세요."
                    )

            except Exception:
                answer = (
                    "⚠️ AI 연결 중 문제가 발생했어요.\n\n"
                    "API 키와 인터넷 연결 상태를 "
                    "확인한 후 다시 시도해 주세요."
                )

        st.markdown(answer)

    # 답변 저장
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# -----------------------------
# 대화 초기화
# -----------------------------
st.write("")

if st.button(
    "🗑️ 대화 처음부터 시작하기",
    use_container_width=True
):
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME}
    ]
    st.rerun()

st.markdown("""
<div class="footer">
    💚 누구나 쉽게 이용하는 지하철 안내<br>
    Easy Metro AI Assistant
</div>
""", unsafe_allow_html=True)

st.caption(
    "⚠️ AI 답변에는 오류가 있을 수 있습니다. "
    "실제 이동 전에는 공식 지하철 노선도와 "
    "운행 정보를 확인해 주세요."
)
