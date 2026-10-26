

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="졸업어때?",
    page_icon="💤",
    layout="centered"
)

# 디자인
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f1f5ff 0%, #ffffff 65%);
    color: #28345c;
}
.block-container {
    max-width: 760px;
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #344a9a !important;
}
.hero {
    background: linear-gradient(120deg, #dce7ff, #f0eaff);
    padding: 26px;
    border-radius: 25px;
    margin-bottom: 18px;
}
.hero h1 {
    margin: 0;
    font-size: 2.3rem !important;
}
.hero p {
    margin: 8px 0 0;
    color: #55638b;
}
.note {
    background: #eef2ff;
    border-radius: 16px;
    padding: 16px;
    margin: 12px 0;
    color: #465585;
}
div.stButton > button[kind="primary"] {
    background: #7475ed;
    border: 0;
    border-radius: 15px;
}
div[data-testid="stMetric"] {
    background: #eef2ff;
    border-radius: 15px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)

SUBJECTS = [
    "국어 📖", "수학 📐", "영어 🔤",
    "사회 🌍", "과학 🔬", "체육 🏃", "기타 ✏️"
]

LEVELS = {
    1: "😊 말똥말똥",
    2: "🙂 조금 나른함",
    3: "😐 졸음이 옴",
    4: "😴 많이 졸림",
    5: "💤 거의 잠듦"
}

# 기록 저장
if "records" not in st.session_state:
    st.session_state.records = []

# 메인 화면
st.markdown("""
<div class="hero">
    <h1>💤 졸업어때?</h1>
    <p>졸음은 기록하고, 수업은 더 집중되게!</p>
</div>
""", unsafe_allow_html=True)

st.caption(
    "잠깐 졸았다고 수업을 포기하지 마세요. "
    "나에게 맞는 집중 방법을 찾아봐요."
)

page = st.radio(
    "메뉴",
    ["📝 졸림 기록", "📊 졸림 분석", "💡 수업 추천"],
    horizontal=True,
    label_visibility="collapsed"
)

# 1. 졸림 기록
if page == "📝 졸림 기록":
    st.subheader("오늘 수업은 어땠나요?")

    with st.form("record_form"):
        subject = st.selectbox("과목 선택", SUBJECTS)

        level = st.select_slider(
            "졸림 정도",
            options=list(LEVELS),
            value=3,
            format_func=lambda n: LEVELS[n]
        )

        period = st.selectbox("교시", list(range(1, 9)))

        memo = st.text_input(
            "메모 (선택)",
            placeholder="예: 점심 먹고 나서 졸렸어요"
        )

        submitted = st.form_submit_button(
            "💜 졸림 기록하기",
            type="primary",
            use_container_width=True
        )

    if submitted:
        st.session_state.records.append({
            "기록시각": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "과목": subject,
            "교시": period,
            "졸림": level,
            "메모": memo
        })

        st.success("기록했어요! 아래에서 맞춤 추천을 확인하세요.")

    if st.session_state.records:
        latest = st.session_state.records[-1]

        st.markdown(
            f'<div class="note">최근 기록: '
            f'<b>{latest["과목"]}</b> · '
            f'{LEVELS[latest["졸림"]]}</div>',
            unsafe_allow_html=True
        )

        if latest["졸림"] >= 4:
            st.info(
                "많이 졸리다면 짧게 몸을 움직이고, "
                "놓친 설명은 친구나 선생님께 확인해 보세요."
            )
        elif latest["졸림"] >= 3:
            st.info(
                "핵심 단어 3개를 적거나 "
                "짝과 질문 하나를 주고받아 보세요."
            )
        else:
            st.info(
                "좋아요! 지금 집중할 수 있을 때 "
                "중요한 내용을 정리해 보세요."
            )

# 2. 졸림 분석
elif page == "📊 졸림 분석":
    st.subheader("나의 졸림 패턴")

    if not st.session_state.records:
        st.info(
            "먼저 '졸림 기록' 메뉴에서 "
            "기록을 추가해 주세요."
        )
    else:
        df = pd.DataFrame(st.session_state.records)

        a, b = st.columns(2)

        a.metric("기록 횟수", f"{len(df)}회")
        b.metric(
            "평균 졸림",
            f"{df['졸림'].mean():.1f} / 5"
        )

        st.write("**과목별 평균 졸림**")

        st.bar_chart(
            df.groupby("과목")["졸림"].mean().sort_values(),
            horizontal=True
        )

        st.write("**교시별 평균 졸림**")

        st.line_chart(
            df.groupby("교시")["졸림"].mean()
        )

        st.dataframe(
            df.iloc[::-1],
            hide_index=True,
            use_container_width=True
        )

        st.download_button(
            "📥 기록 CSV 저장",
            df.to_csv(index=False).encode("utf-8-sig"),
            "sleep_records.csv",
            "text/csv"
        )

        if st.button("🗑️ 내 기록 초기화"):
            st.session_state.records = []
            st.rerun()

# 3. 수업 추천
else:
    st.subheader("졸림 정도에 맞는 수업 방법")

    st.caption(
        "교사가 학생들의 상태를 참고해 "
        "수업을 조절할 때 활용할 수 있어요."
    )

    if st.session_state.records:
        average = (
            sum(r["졸림"] for r in st.session_state.records)
            / len(st.session_state.records)
        )

        st.metric("현재 기록 평균", f"{average:.1f} / 5")

        default_level = min(5, max(1, round(average)))
    else:
        default_level = 3

    selected = st.slider(
        "추천받을 졸림 단계",
        1, 5, default_level
    )

    if selected <= 2:
        st.success("🟢 집중 상태가 좋아요")

        st.markdown(
            "**추천:** 개념 설명 15분 → "
            "문제 해결 15분 → 핵심 정리 5분"
        )

    elif selected == 3:
        st.warning("🟡 집중 전환이 필요해요")

        st.markdown(
            "**추천:** 짧은 설명 10분 → "
            "짝 토의 5분 → 퀴즈 10분 → 정리 5분"
        )

    else:
        st.error("🔴 졸림이 높은 상태예요")

        st.markdown(
            "**추천:** 가벼운 스트레칭 2분 → "
            "참여형 활동 10분 → 짧은 설명 5분 → "
            "확인 퀴즈 5분"
        )

    st.markdown("""
    <div class="note">
    💡 졸림 정도만으로 수업의 난이도를 자동 결정하지는 않아요.
    학습 목표와 학생 상태를 함께 고려하세요.
    </div>
    """, unsafe_allow_html=True)

    st.write("**놓친 수업 따라잡기**")
    st.write(
        "① 친구의 필기 확인하기  "
        "② 핵심 개념 3개 적기  "
        "③ 이해 안 된 부분 질문하기"
    )

st.divider()

st.caption(
    "💜 졸업어때? | 기록은 현재 브라우저 세션에서만 유지됩니다. "
    "새로 접속하거나 서버가 재시작되면 사라질 수 있어요."
)
