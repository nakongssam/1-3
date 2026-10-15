
import streamlit as st
from datetime import datetime
import random

st.set_page_config(
    page_title="마음쉼표",
    page_icon="🌿",
    layout="centered"
)

# 화면 디자인
st.markdown("""
<style>
.stApp {
    background-color: #F5FAF6;
}
h1, h2, h3 {
    color: #326B50;
}
.stButton > button {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# 기록 저장 (현재 접속 동안 유지)
if "records" not in st.session_state:
    st.session_state.records = []

st.title("🌿 마음쉼표")
st.write("잠깐 쉬어가도 괜찮아요.")
st.caption("나의 스트레스를 알아보고 마음을 돌보는 작은 공간")

tab1, tab2, tab3, tab4 = st.tabs([
    "💚 스트레스 체크",
    "📝 감정 일기",
    "🧘 마음 안정",
    "📊 나의 기록"
])

# 1. 스트레스 체크
with tab1:
    st.subheader("오늘 스트레스는 어느 정도인가요?")

    score = st.slider(
        "스트레스 정도",
        min_value=0,
        max_value=10,
        value=5
    )

    if score <= 3:
        st.success("😊 비교적 편안한 상태예요.")
        activities = [
            "좋아하는 음악 듣기 🎵",
            "가볍게 산책하기 🚶",
            "오늘 감사한 일 떠올리기 💚"
        ]
    elif score <= 6:
        st.warning("🌼 조금 지쳐 있을 수 있어요.")
        activities = [
            "5분간 스트레칭하기",
            "잠깐 스마트폰 내려놓기",
            "따뜻한 차 마시기 🍵"
        ]
    else:
        st.error("💗 스트레스가 높게 느껴지는군요.")
        activities = [
            "조용한 곳에서 잠시 쉬기",
            "천천히 호흡하기",
            "믿을 만한 사람과 이야기하기"
        ]

    if st.button("✨ 나에게 맞는 활동 추천"):
        st.info(random.choice(activities))

    if st.button("💾 스트레스 점수 저장"):
        st.session_state.records.append({
            "시간": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "스트레스": score,
            "기분": "-",
            "내용": ""
        })
        st.success("기록을 저장했어요!")

# 2. 감정 일기
with tab2:
    st.subheader("오늘 내 마음은 어떤가요?")

    mood = st.radio(
        "현재 기분을 선택해 주세요.",
        ["😊 행복", "😌 평온", "😐 보통",
         "😟 불안", "😢 슬픔", "😡 화남"],
        horizontal=True
    )

    diary = st.text_area(
        "오늘 어떤 일이 있었나요?",
        placeholder="마음에 남는 일을 자유롭게 적어보세요."
    )

    if st.button("📝 일기 저장"):
        if diary.strip():
            st.session_state.records.append({
                "시간": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "스트레스": None,
                "기분": mood,
                "내용": diary.strip()
            })
            st.success("오늘의 마음을 기록했어요 💚")
        else:
            st.warning("일기 내용을 입력해 주세요.")

# 3. 마음 안정
with tab3:
    st.subheader("🧘 잠깐 마음을 쉬게 해주세요")

    st.write("편안하게 앉아서 천천히 호흡해 보세요.")

    st.markdown("""
    ### 🌬️ 간단한 호흡 운동

    1. 🌿 4초 동안 천천히 숨 들이마시기
    2. ⏸️ 4초 동안 편안하게 멈추기
    3. 🍃 6초 동안 천천히 숨 내쉬기

    무리하지 말고 자신의 호흡에 맞춰 반복하세요.
    """)

    st.divider()

    messages = [
        "모든 일을 완벽하게 해낼 필요는 없어요.",
        "잠깐 쉬는 것도 중요한 일이에요.",
        "오늘도 충분히 애쓰고 있어요.",
        "내 감정을 알아차리는 것부터 시작해요.",
        "천천히 가도 괜찮아요."
    ]

    if st.button("💌 마음을 위한 한마디"):
        st.info(random.choice(messages))

# 4. 나의 기록
with tab4:
    st.subheader("📊 나의 마음 기록")

    records = st.session_state.records

    if not records:
        st.info("아직 기록이 없어요. 오늘의 마음을 기록해 보세요!")
    else:
        scores = [
            r["스트레스"] for r in records
            if r["스트레스"] is not None
        ]

        if scores:
            average = sum(scores) / len(scores)
            st.metric("평균 스트레스 점수", f"{average:.1f} / 10")

            st.line_chart(
                {"스트레스 점수": scores},
                y_label="스트레스 정도"
            )

        st.divider()
        st.write("### 📖 기록 목록")

        for record in reversed(records):
            with st.expander(
                f'{record["시간"]} | {record["기분"]}'
            ):
                if record["스트레스"] is not None:
                    st.write(
                        f'스트레스: {record["스트레스"]}/10'
                    )
                if record["내용"]:
                    st.write(record["내용"])

        if st.button("🗑️ 전체 기록 삭제"):
            st.session_state.records = []
            st.rerun()

st.divider()
st.caption(
    "🌿 마음쉼표는 자기 돌봄을 위한 앱이며 "
    "의학적 진단이나 전문 상담을 대신하지 않습니다."
)
