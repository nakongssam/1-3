
import streamlit as st
from google import genai
from google.genai import types

# 1. 페이지 설정
st.set_page_config(
    page_title="연애 고민 상담소",
    page_icon="💘",
    layout="centered"
)

# 2. 화면 디자인
st.markdown("""
<style>
    .stApp {
        background-color: #fff9fb;
    }
    h1, h2, h3 {
        color: #d94f78;
    }
    .stButton button {
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.title("💘 연애 고민 상담소")
st.write("혼자 고민하지 말고, AI 연애 상담사에게 이야기해 보세요!")
st.caption("💌 썸부터 이별까지, 당신의 마음을 함께 정리해 드려요.")

st.divider()

# 3. API 키 확인
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("⚠️ GEMINI_API_KEY가 설정되지 않았습니다.")
    st.info("Streamlit Cloud의 Secrets에 API 키를 등록해 주세요.")
    st.stop()

if not api_key:
    st.error("API 키가 비어 있습니다.")
    st.stop()

# 4. 상담 유형
categories = {
    "💗 썸·짝사랑": "좋아하는 사람에게 먼저 연락해도 될까요?",
    "💕 연애 중": "연인과 자주 다투는데 어떻게 해결할까요?",
    "💔 이별·재회": "헤어진 사람을 잊기 어려워요.",
    "💌 고백·연락": "좋아하는 사람에게 보낼 메시지를 추천해 주세요.",
    "🌷 자유 상담": "제 연애 고민을 들어주세요."
}

st.subheader("어떤 고민이 있나요?")

category = st.selectbox(
    "상담 주제를 선택하세요.",
    list(categories.keys())
)

# 5. 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "category" not in st.session_state:
    st.session_state.category = category

# 상담 유형 변경 시 대화 초기화
if st.session_state.category != category:
    st.session_state.messages = []
    st.session_state.category = category

# 6. 빠른 질문과 초기화
col1, col2 = st.columns([3, 1])

with col1:
    quick_question = st.button(
        "✨ 추천 질문으로 상담하기",
        use_container_width=True
    )

with col2:
    if st.button("🔄 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 7. AI 상담사 역할 설정
system_prompt = """
너는 친절하고 따뜻한 한국어 연애 상담사야.

상담 원칙:
1. 사용자의 감정을 먼저 공감해 줘.
2. 현실적이고 구체적인 조언을 제공해.
3. 상대방의 마음을 확실하게 안다고 단정하지 마.
4. 필요하다면 실제로 보낼 수 있는 메시지 예시를 작성해.
5. 답변은 너무 길지 않게 3~5문단으로 작성해.
6. 친근하고 자연스러운 한국어를 사용해.
7. 이모지는 적절히 사용해.
8. 사용자의 선택과 상대방의 동의를 존중해.
9. 집착, 감시, 협박, 폭력을 정당화하지 마.
10. 위협이나 폭력 상황에서는 안전을 우선하도록 안내해.
"""

# 8. 기존 대화 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. 사용자 질문 입력
user_input = st.chat_input("연애 고민을 자유롭게 입력하세요...")

if quick_question:
    user_input = categories[category]

# 10. Gemini API 호출
if user_input and user_input.strip():

    user_input = user_input.strip()

    with st.chat_message("user"):
        st.markdown(user_input)

    # API 요청에 사용할 대화 기록
    history = st.session_state.messages[-18:]

    contents = []

    for message in history:
        role = "user" if message["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ]
            )
        )

    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)]
        )
    )

    with st.chat_message("assistant"):
        with st.spinner("💗 답변을 생각하고 있어요..."):
            try:
                client = genai.Client(api_key=api_key)

                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.7,
                        max_output_tokens=1500
                    )
                )

                answer = response.text

                if not answer:
                    raise ValueError("AI 응답이 비어 있습니다.")

                st.markdown(answer)

                # 성공한 대화만 기록
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_input
                })

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                error_text = str(e).lower()

                if "429" in error_text or "resource_exhausted" in error_text:
                    st.error("요청이 너무 많아요. 잠시 후 다시 시도해 주세요.")
                elif "api_key" in error_text or "403" in error_text:
                    st.error("API 키 또는 API 사용 권한을 확인해 주세요.")
                elif "404" in error_text:
                    st.error("AI 모델을 찾을 수 없습니다. 모델 사용 가능 여부를 확인해 주세요.")
                else:
                    st.error("상담 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")

st.divider()
st.caption(
    "💌 AI의 답변은 참고용입니다. "
    "개인정보나 타인의 민감한 정보는 입력하지 마세요."
)
