
import streamlit as st
from datetime import datetime
import random

# ---------------------------------
# 1. 기본 설정
# ---------------------------------
st.set_page_config(
    page_title="마음쉼표 - 스트레스 관리",
    page_icon="🌿",
    layout="centered"
)

# 디자인
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

# ---------------------------------
# 2. 데이터 초기화
# ---------------------------------
if "records" not in st.session_state:
    st.session_state.records = []

if "message" not in st.session_state:
    st.session_state.message = "오늘도 충분히 잘하고 있어요. 🌷"

# ---------------------------------
# 3. 앱 제목
# ---------------------------------
st.title("🌿 마음쉼표")
st.caption("하루 3분, 내 마음을 돌보는 시간")
st.divider()

tab1, tab2, tab3 = st.tabs([
    "😊 오늘의 마음",
    "🌬️ 마음 돌보기",
    "📊 나의 기록"
])

# ---------------------------------
# 4. 오늘의 마음
# ---------------------------------
with tab1:
    st.header("오늘 기분은 어떤가요?")
    st.write("지금 느끼는 스트레스를 숫자로 표현해 보세요.")

    stress = st.slider(
        "스트레스 정도",
        min_value=0,
        max_value=10,
        value=5
    )

    if stress <= 3:
        st.success("😊 비교적 편안한 상태예요!")
        advice = "좋은 기분을 유지하며 가볍게 산책해 보세요."
    elif stress <= 6:
        st.warning("😐 조금 지쳐 있을 수 있어요.")
        advice = "잠시 쉬면서 좋아하는 음악을 들어보세요."
    else:
        st.error("😥 스트레스가 높은 상태예요.")
        advice = "무리하지 말고 휴식과 깊은 호흡을 해보세요."

    st.info("💡 오늘의 추천: " + advice)

    emotion = st.selectbox(
        "지금 느끼는 감정",
        ["😊 행복", "😌 평온", "😐 보통",
         "😟 불안", "😢 슬픔", "😡 화남", "😴 피곤"]
    )

    reason = st.selectbox(
        "스트레스의 주요 원인은?",
        ["학업", "직장", "인간관계", "가족",
         "건강", "미래 고민", "기타", "특별히 없음"]
    )

    diary = st.text_area(
        "오늘의 마음을 자유롭게 적어보세요.",
        placeholder="오늘 어떤 일이 있었나요?"
    )

    if st.button("💚 오늘의 마음 기록하기", use_container_width=True):
        try:
            record = {
                "날짜": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "스트레스": stress,
                "감정": emotion,
                "원인": reason,
                "일기": diary.strip()
            }

            st.session_state.records.append(record)
            st.success("오늘의 마음이 기록되었어요! 🌱")
            st.balloons()

        except Exception:
            st.error("기록 중 문제가 발생했어요. 다시 시도해 주세요.")

# ---------------------------------
# 5. 마음 돌보기
# ---------------------------------
with tab2:
    st.header("🌬️ 잠깐, 숨을 쉬어볼까요?")
    st.write("천천히 호흡하며 몸과 마음을 편안하게 해보세요.")

    st.markdown("""
    ### 🌿 간단한 호흡 운동

    1. 코로 천천히 **4초 동안 숨을 들이마셔요.**
    2. 편안하다면 **4초 동안 숨을 멈춰요.**
    3. 입으로 천천히 **6초 동안 숨을 내쉬어요.**
    4. 이 과정을 3~5회 반복해요.

    숨을 참기 불편하다면 멈추지 않고
    자연스럽게 호흡해도 괜찮아요.
    """)

    if st.button("🌬️ 호흡 가이드 시작", use_container_width=True):
        guide = st.empty()
        progress = st.progress(0)

        import time

        try:
            steps = [
                ("🌬️ 숨을 들이마셔요", 4),
                ("🍃 편안하게 멈춰요", 4),
                ("💨 천천히 내쉬어요", 6)
            ]

            total = sum(seconds for _, seconds in steps) * 3
            elapsed = 0

            for cycle in range(3):
                for title, seconds in steps:
                    for remaining in range(seconds, 0, -1):
                        guide.info(
                            f"{cycle + 1}/3회 | {title} "
                            f"({remaining}초)"
                        )
                        time.sleep(1)
                        elapsed += 1
                        progress.progress(min(elapsed / total, 1.0))

            guide.success("✨ 호흡 운동을 완료했어요!")
        except Exception:
            st.error("호흡 가이드를 실행하지 못했어요.")

    st.divider()
    st.subheader("🎯 나에게 맞는 스트레스 해소법")

    activity = st.selectbox(
        "지금 하고 싶은 활동을 선택하세요.",
        ["몸을 움직이고 싶어요",
         "조용히 쉬고 싶어요",
         "기분 전환이 필요해요",
         "생각을 정리하고 싶어요"]
    )

    recommendations = {
        "몸을 움직이고 싶어요": [
            "🚶 10분 동안 가볍게 산책하기",
            "🧘 목과 어깨 스트레칭하기",
            "💃 좋아하는 노래에 맞춰 움직이기"
        ],
        "조용히 쉬고 싶어요": [
            "🍵 따뜻한 차 마시기",
            "🌿 눈 감고 3분 쉬기",
            "🛏️ 잠시 누워서 몸의 긴장 풀기"
        ],
        "기분 전환이 필요해요": [
            "🎵 좋아하는 음악 듣기",
            "🎨 그림 그리기",
            "🌳 창밖 풍경 바라보기"
        ],
        "생각을 정리하고 싶어요": [
            "📝 걱정되는 일 적어보기",
            "💚 오늘 감사한 일 3가지 찾기",
            "📋 지금 할 수 있는 일 하나 정하기"
        ]
    }

    for item in recommendations[activity]:
        st.write(item)

    st.divider()
    st.subheader("💌 오늘의 응원")

    messages = [
        "오늘도 충분히 잘하고 있어요. 🌷",
        "잠깐 쉬어가도 괜찮아요. 🍀",
        "모든 일을 완벽하게 할 필요는 없어요.",
        "작은 행복도 소중한 행복이에요. 💚",
        "지금 이 순간의 나를 아껴주세요.",
        "천천히 가도 괜찮아요. 🌿",
        "힘든 날에는 쉬는 것도 중요한 일이에요."
    ]

    if st.button("💌 새로운 응원 받기"):
        st.session_state.message = random.choice(messages)

    st.info(st.session_state.message)

# ---------------------------------
# 6. 나의 기록
# ---------------------------------
with tab3:
    st.header("📊 나의 마음 기록")

    records = st.session_state.records

    if not records:
        st.info("아직 기록이 없어요. 오늘의 마음을 기록해 보세요.")
    else:
        try:
            scores = [r["스트레스"] for r in records]
            average = sum(scores) / len(scores)

            col1, col2, col3 = st.columns(3)

            col1.metric("기록 횟수", f"{len(records)}회")
            col2.metric("평균 스트레스", f"{average:.1f}점")
            col3.metric("최근 스트레스", f"{scores[-1]}점")

            st.subheader("📈 스트레스 변화")
            st.line_chart(
                {"스트레스 점수": scores},
                y_label="스트레스 점수"
            )

            st.subheader("📖 마음 일기")

            for record in reversed(records):
                with st.expander(
                    f"{record['날짜']} | "
                    f"{record['감정']} | "
                    f"{record['스트레스']}점"
                ):
                    st.write("**원인:**", record["원인"])
                    st.write(
                        "**오늘의 기록:**",
                        record["일기"] or "작성한 내용이 없어요."
                    )

            st.divider()

            # CSV 다운로드
            import csv
            import io

            output = io.StringIO()
            writer = csv.DictWriter(
                output,
                fieldnames=["날짜", "스트레스", "감정", "원인", "일기"]
            )
            writer.writeheader()
            writer.writerows(records)

            csv_data = output.getvalue().encode("utf-8-sig")

            st.download_button(
                "📥 내 마음 기록 다운로드 (CSV)",
                data=csv_data,
                file_name="마음쉼표_기록.csv",
                mime="text/csv",
                use_container_width=True
            )

            if st.button("🗑️ 모든 기록 삭제"):
                st.session_state.records = []
                st.rerun()

        except Exception:
            st.error("기록을 표시하는 중 문제가 발생했어요.")

# ---------------------------------
# 7. 하단 안내
# ---------------------------------
st.divider()
st.caption(
    "🌿 마음쉼표 | 나를 위한 작은 휴식"
)
st.caption(
    "이 앱은 일상적인 스트레스 관리를 돕는 도구이며 "
    "의학적 진단이나 치료를 대신하지 않습니다."
)
st.caption(
    "기록은 현재 접속 세션에만 저장됩니다. "
    "브라우저를 새로고침하거나 세션이 종료되면 "
    "기록이 사라질 수 있으니 CSV로 다운로드하세요."
)
