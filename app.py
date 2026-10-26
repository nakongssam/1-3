
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="졸업어때? | SLEEP LAB",
    page_icon="💤",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------
# 디자인
# -----------------------
st.markdown("""
<style>
.stApp {
    background: #E84B25;
}
.block-container {
    max-width: 600px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
h1, h2, h3, p, label {
    font-family: 'Arial', sans-serif;
}
.hero {
    background: #39235E;
    border-radius: 28px;
    padding: 28px 24px;
    color: white;
    margin-bottom: 20px;
}
.hero .small {
    color: #FFE16B;
    font-size: 13px;
    letter-spacing: 3px;
    font-weight: bold;
}
.hero h1 {
    font-size: clamp(3rem, 12vw, 5rem);
    line-height: 1;
    letter-spacing: -3px;
    color: white !important;
    margin: 18px 0;
    font-weight: 900;
}
.hero .desc {
    color: #E7DFFF;
    font-size: 15px;
}
.hero .moon {
    font-size: 55px;
    text-align: right;
}
div[data-testid="stChatMessage"] {
    border-radius: 20px;
    padding: 14px;
    margin-bottom: 12px;
}
div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-user"]
) {
    background: #FFE16B;
    color: #271944;
}
div[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    background: #39235E;
    color: white;
}
div[data-testid="stChatMessage"] p {
    color: inherit;
}
div[data-testid="stChatMessage"] * {
    overflow-wrap: anywhere;
}
div.stButton > button {
    border-radius: 30px;
    border: 2px solid #39235E;
    background: #FFE16B;
    color: #39235E;
    font-weight: 800;
    min-height: 44px;
}
div.stButton > button:hover {
    background: white;
    color: #39235E;
    border-color: #39235E;
}
div[data-testid="stChatInput"] {
    border-radius: 18px;
}
div[data-testid="stMetric"] {
    background: #FFE16B;
    padding: 16px;
    border-radius: 18px;
}
div[data-testid="stMetric"] * {
    color: #39235E;
}
[data-testid="stRadio"] label {
    color: white;
    font-weight: bold;
}
[data-testid="stCaptionContainer"] {
    color: #FFF3E9;
}
.section-title {
    color: white;
    font-size: 24px;
    font-weight: 900;
    margin: 18px 0;
}
.result-card {
    background: #39235E;
    color: white;
    padding: 22px;
    border-radius: 24px;
    margin: 12px 0;
}
.result-card h3 {
    color: #FFE16B !important;
}
</style>
""", unsafe_allow_html=True)

SUBJECTS = [
    "국어", "수학", "영어", "사회",
    "과학", "체육", "기타"
]

# -----------------------
# 세션 상태
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "HEY! 👋 오늘도 수업 듣느라 고생했어!\n\n"
            "어떤 과목에서 졸렸어?\n"
            "국어, 수학, 영어, 사회, 과학, 체육 중 알려줘!"
        )
    }]

if "step" not in st.session_state:
    st.session_state.step = "subject"

if "subject" not in st.session_state:
    st.session_state.subject = None

if "level" not in st.session_state:
    st.session_state.level = None

if "records" not in st.session_state:
    st.session_state.records = []


def bot_say(message):
    st.session_state.messages.append({
        "role": "assistant",
        "content": message
    })


def user_say(message):
    st.session_state.messages.append({
        "role": "user",
        "content": message
    })


def get_level(message):
    for char in message:
        if char in "12345":
            return int(char)

    words = {
        "안 졸": 1,
        "멀쩡": 1,
        "조금": 2,
        "보통": 3,
        "많이": 4,
        "너무": 5,
        "매우": 5,
        "잠들": 5
    }

    for word, number in words.items():
        if word in message:
            return number

    return None


def recommendation(level):
    if level <= 2:
        return (
            "🟢 집중력이 좋은 상태야!\n\n"
            "추천 수업 방식:\n"
            "개념 설명 15분 → 문제 해결 15분 → 정리 5분\n\n"
            "지금 중요한 내용을 정리하면 좋겠어!"
        )

    if level == 3:
        return (
            "🟡 살짝 졸린 상태구나!\n\n"
            "추천 수업 방식:\n"
            "짧은 설명 10분 → 짝 토의 5분 → "
            "퀴즈 10분\n\n"
            "핵심 단어 3개를 적어보자!"
        )

    return (
        "🔴 졸음이 많이 몰려오는구나!\n\n"
        "추천 수업 방식:\n"
        "가벼운 스트레칭 2분 → 참여 활동 10분 → "
        "짧은 설명 5분\n\n"
        "놓친 부분은 친구의 필기를 확인하거나 "
        "선생님께 질문해 봐!"
    )


def handle_message(message):
    message = message.strip()

    if not message:
        return

    user_say(message)
    step = st.session_state.step

    if step == "subject":
        found = None

        for subject in SUBJECTS:
            if subject in message:
                found = subject
                break

        if found is None:
            bot_say(
                "어떤 과목인지 잘 모르겠어! 😅\n\n"
                "국어, 수학, 영어, 사회, 과학, 체육, 기타 "
                "중 하나를 입력해 줘."
            )
            return

        st.session_state.subject = found
        st.session_state.step = "level"

        bot_say(
            f"오! {found} 시간이었구나! 📚\n\n"
            "얼마나 졸렸어?\n\n"
            "1️⃣ 전혀 안 졸림\n"
            "2️⃣ 조금 나른함\n"
            "3️⃣ 졸음이 옴\n"
            "4️⃣ 많이 졸림\n"
            "5️⃣ 거의 잠듦\n\n"
            "숫자 1~5로 알려줘!"
        )

    elif step == "level":
        level = get_level(message)

        if level is None:
            bot_say(
                "졸림 정도를 1부터 5 사이의 숫자로 "
                "입력해 줘! 💤"
            )
            return

        st.session_state.level = level
        st.session_state.step = "memo"

        bot_say(
            "좋아! 기록하기 전에 하나만 더 물어볼게.\n\n"
            "왜 졸렸던 것 같아?\n\n"
            "예: 점심 먹고 나서, 잠을 못 자서, "
            "설명이 길어서\n\n"
            "이유가 없으면 '없음'이라고 입력해 줘!"
        )

    elif step == "memo":
        subject = st.session_state.subject
        level = st.session_state.level

        st.session_state.records.append({
            "시간": datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),
            "과목": subject,
            "졸림": level,
            "이유": message
        })

        bot_say(
            f"💜 기록 완료!\n\n"
            f"과목: {subject}\n\n"
            f"졸림 정도: {level}/5\n\n"
            f"이유: {message}\n\n"
            f"{recommendation(level)}\n\n"
            "다른 과목도 기록하고 싶으면 "
            "'다시'라고 입력해 줘!"
        )

        st.session_state.step = "done"

    elif step == "done":
        if any(word in message for word in [
            "다시", "시작", "기록", "추가"
        ]):
            st.session_state.step = "subject"
            bot_say(
                "좋아! 다시 시작해 보자! ✨\n\n"
                "이번에는 어떤 과목에서 졸렸어?"
            )
        elif "분석" in message:
            bot_say(
                "상단의 📊 ANALYSIS 메뉴에서 "
                "과목별 졸림 기록을 확인할 수 있어!"
            )
        else:
            bot_say(
                "다른 과목도 기록하려면 '다시', "
                "기록을 분석하려면 '분석'이라고 입력해 줘!"
            )


# -----------------------
# 메인 디자인
# -----------------------
st.markdown("""
<div class="hero">
    <div class="small">SLEEP LAB — 2026</div>
    <h1>졸업<br>어때?</h1>
    <div class="moon">🌙💤</div>
    <div class="desc">
        졸음은 기록하고,<br>
        수업은 더 집중되게.
    </div>
</div>
""", unsafe_allow_html=True)

menu = st.radio(
    "메뉴",
    ["💬 CHAT", "📊 ANALYSIS"],
    horizontal=True,
    label_visibility="collapsed"
)

# -----------------------
# 챗봇 화면
# -----------------------
if menu == "💬 CHAT":
    st.markdown(
        '<div class="section-title">LET’S TALK. 💬</div>',
        unsafe_allow_html=True
    )

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if st.session_state.step == "subject":
        st.caption("과목을 선택하거나 직접 입력해 봐!")
        cols = st.columns(3)

        for index, subject in enumerate(SUBJECTS[:6]):
            with cols[index % 3]:
                if st.button(
                    subject,
                    key=f"subject_{index}",
                    use_container_width=True
                ):
                    handle_message(subject)
                    st.rerun()

    elif st.session_state.step == "level":
        st.caption("지금 졸림 정도는?")
        cols = st.columns(5)

        for i in range(1, 6):
            with cols[i - 1]:
                if st.button(
                    str(i),
                    key=f"level_{i}",
                    use_container_width=True
                ):
                    handle_message(str(i))
                    st.rerun()

    elif st.session_state.step == "memo":
        if st.button(
            "이유 없음 → 바로 기록",
            use_container_width=True
        ):
            handle_message("없음")
            st.rerun()

    else:
        if st.button(
            "✨ 다른 과목 기록하기",
            use_container_width=True
        ):
            handle_message("다시")
            st.rerun()

    prompt = st.chat_input(
        "여기에 답변을 입력해 줘..."
    )

    if prompt:
        handle_message(prompt)
        st.rerun()

# -----------------------
# 분석 화면
# -----------------------
else:
    st.markdown(
        '<div class="section-title">YOUR SLEEP DATA.</div>',
        unsafe_allow_html=True
    )

    records = st.session_state.records

    if not records:
        st.info(
            "아직 기록이 없어! "
            "CHAT 메뉴에서 첫 기록을 남겨 봐."
        )
    else:
        df = pd.DataFrame(records)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("TOTAL RECORDS", len(df))

        with col2:
            st.metric(
                "SLEEP SCORE",
                f"{df['졸림'].mean():.1f}/5"
            )

        st.markdown(
            '<div class="section-title">SUBJECT RANKING.</div>',
            unsafe_allow_html=True
        )

        summary = (
            df.groupby("과목")["졸림"]
            .mean()
            .sort_values(ascending=False)
        )

        st.bar_chart(summary)

        sleepiest = summary.index[0]

        st.markdown(
            f'<div class="result-card">'
            f'<h3>MOST SLEEPY 😴</h3>'
            f'<p>가장 졸렸던 과목은 '
            f'<b>{sleepiest}</b>!</p>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">HISTORY.</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df.iloc[::-1],
            hide_index=True,
            use_container_width=True
        )

        st.download_button(
            "📥 기록 다운로드",
            data=df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="sleep_records.csv",
            mime="text/csv",
            use_container_width=True
        )

        if st.button(
            "🗑️ 기록 초기화",
            use_container_width=True
        ):
            st.session_state.records = []
            st.session_state.messages = [{
                "role": "assistant",
                "content": (
                    "다시 시작해 보자! 💜\n\n"
                    "어떤 과목에서 졸렸어?"
                )
            }]
            st.session_state.step = "subject"
            st.session_state.subject = None
            st.session_state.level = None
            st.rerun()

st.markdown("---")
st.caption(
    "SLEEP LAB © 2026 | 졸업어때? 💜 "
    "현재 접속 세션에서만 기록이 유지됩니다."
)
