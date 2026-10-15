
import streamlit as st
from google import genai

# ------------------------------------
# 1. 기본 설정
# ------------------------------------
st.set_page_config(
    page_title="마음쉼표 AI",
    page_icon="🌿",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #F7FAF7;
}
h1, h2, h3 {
    color: #315B46;
}
div.stButton > button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------
# 2. 세션 초기화
# ------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "stress" not in st.session_state:
    st.session_state.stress = 5

# ------------------------------------
# 3. API 키 확인
# ------------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    if not api_key:
        st.error("GEMINI_API_KEY가 비어 있습니다.")
        st.stop()

    client = genai.Client(api_key=api_key)

except Exception:
    st.error(
        "Gemini API 키를 확인할 수 없습니다. "
        "Streamlit Secrets에 GEMINI_API_KEY를 설정하세요."
    )
    st.stop()

# ------------------------------------
# 4. 사이드바
# ------------------------------------
with st.sidebar:
    st.title("🌿 마음 관리")

    st.subheader("😊 현재 스트레스 정도")

    stress = st.slider(
        "지금 스트레스는 몇 점인가요?",
        min_value=0,
        max_value=10,
        value=st.session_state.stress
    )

    st.session_state.stress = stress

    if stress <= 3:
        st.success("마음이 비교적 편안한 상태예요.")
    elif stress <= 6:
        st.warning("조금 지쳐 있을 수 있어요.")
    else:
        st.error("스트레스가 높은 상태예요.")

    st.divider()

    st.subheader("🎯 상담 주제")
    topic = st.selectbox(
        "어떤 이야기를 나누고 싶나요?",
        [
            "자유롭게 이야기하기",
            "📚 공부와 시험 스트레스",
            "👥 친구와 인간관계",
            "🏠 가족과의 갈등",
            "😟 불안과 걱정",
            "😴 피로와 무기력",
            "🌱 자존감과 자신감"
        ]
    )

    st.divider()

    if st.button("🔄 새로운 대화 시작", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "대화 내용은 현재 접속 세션에만 유지됩니다."
    )

# ------------------------------------
# 5. 메인 화면
# ------------------------------------
st.title("🌿 마음쉼표 AI")
st.caption("당신의 마음을 들어주는 따뜻한 AI 친구")
st.divider()

st.info(
    "💚 오늘 어떤 일이 있었나요? "
    "힘들었던 일이나 고민을 편하게 이야기해 주세요."
)

# ------------------------------------
# 6. 빠른 질문 버튼
# ------------------------------------
st.subheader("💬 이런 이야기부터 시작해 보세요")

col1, col2 = st.columns(2)

with col1:
    quick1 = st.button(
        "😥 너무 스트레스 받아요",
        use_container_width=True
    )
    quick3 = st.button(
        "😟 미래가 불안해요",
        use_container_width=True
    )

with col2:
    quick2 = st.button(
        "👥 인간관계가 힘들어요",
        use_container_width=True
    )
    quick4 = st.button(
        "🌱 위로가 필요해요",
        use_container_width=True
    )

quick_prompt = None

if quick1:
    quick_prompt = "요즘 스트레스가 너무 심해요."
elif quick2:
    quick_prompt = "인간관계 때문에 마음이 힘들어요."
elif quick3:
    quick_prompt = "미래에 대한 걱정이 많고 불안해요."
elif quick4:
    quick_prompt = "오늘은 따뜻한 위로가 필요해요."

st.divider()

# ------------------------------------
# 7. 기존 채팅 표시
# ------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------------------
# 8. 사용자 입력
# ------------------------------------
user_input = st.chat_input(
    "지금 마음속 이야기를 들려주세요..."
)

prompt = user_input or quick_prompt

# ------------------------------------
# 9. Gemini AI 답변 생성
# ------------------------------------
if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("마음을 담아 답변하고 있어요..."):

            system_prompt = f"""
당신은 '마음쉼표'라는 스트레스 관리 AI 챗봇입니다.

사용자의 스트레스를 이해하고,
공감과 실용적인 조언을 제공하는 역할입니다.

현재 사용자의 스트레스 점수: {stress}/10
현재 상담 주제: {topic}

답변 규칙:
1. 항상 한국어로 답변합니다.
2. 따뜻하고 친근한 말투를 사용합니다.
3. 먼저 사용자의 감정을 공감합니다.
4. 무조건 긍정하거나 판단하지 않습니다.
5. 스트레스의 원인을 함께 정리합니다.
6. 실천 가능한 작은 행동을 1~2개 제안합니다.
7. 필요할 때 자연스러운 질문을 하나 합니다.
8. 답변은 너무 길지 않게 작성합니다.
9. 이모지는 적절하게 사용합니다.
10. 정신질환을 진단하거나 치료를 약속하지 않습니다.
11. 전문 상담이나 치료가 필요해 보이면
    전문가의 도움을 권합니다.
12. 자해 또는 자살 위험이 언급되면
    안전 확인을 우선하고 긴급 도움을 안내합니다.
13. 사용자의 개인정보를 불필요하게 요구하지 않습니다.
"""

            try:
                # 이전 대화 포함
                history = []

                for msg in st.session_state.messages[-20:]:
                    role = (
                        "user"
                        if msg["role"] == "user"
                        else "model"
                    )

                    history.append({
                        "role": role,
                        "parts": [
                            {"text": msg["content"]}
                        ]
                    })

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=history,
                    config={
                        "system_instruction": system_prompt,
                        "temperature": 0.7,
                        "max_output_tokens": 1200
                    }
                )

                answer = response.text

                if not answer:
                    answer = (
                        "답변을 생성하지 못했어요. "
                        "잠시 후 다시 이야기해 주세요."
                    )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(
                    "AI 답변을 생성하는 중 문제가 발생했어요. "
                    "잠시 후 다시 시도해 주세요."
                )
                with st.expander("오류 상세 정보"):
                    st.code(str(e))

# ------------------------------------
# 10. 하단 안내
# ------------------------------------
st.divider()

st.caption(
    "🌿 마음쉼표 AI | 오늘도 당신의 마음을 응원합니다."
)

st.caption(
    "이 챗봇은 일상적인 스트레스 관리를 돕는 AI이며 "
    "전문적인 심리 상담이나 의료 서비스를 대체하지 않습니다."
)

st.caption(
    "위급하거나 자신을 해칠 위험이 있다면 "
    "즉시 119 또는 112에 연락하세요."
)
