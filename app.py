import time
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="마음 쉼표", page_icon="🌿", layout="centered")

# ---------------- 세션 초기화 ----------------
if "journal" not in st.session_state:
    st.session_state.journal = []

# ---------------- 사이드바 ----------------
st.sidebar.title("🌿 마음 쉼표")
menu = st.sidebar.radio(
    "메뉴",
    ["🏠 홈", "📋 스트레스 체크", "🫁 호흡 연습", "💡 대처 방법", "📝 감정 일기", "📞 도움 받기"],
)
st.sidebar.caption("고등학교 1학년을 위한 스트레스 관리 앱")

# ---------------- 홈 ----------------
if menu == "🏠 홈":
    st.title("🌿 마음 쉼표")
    st.subheader("오늘 내 마음은 어떤가요?")
    mood = st.select_slider(
        "지금 기분을 골라보세요",
        options=["😣 많이 힘듦", "😟 조금 힘듦", "😐 보통", "🙂 괜찮음", "😄 좋음"],
        value="😐 보통",
    )
    if mood in ["😣 많이 힘듦", "😟 조금 힘듦"]:
        st.info("힘든 하루였군요. 왼쪽 메뉴의 **호흡 연습**부터 해볼까요? 3분이면 충분해요.")
    else:
        st.success("좋아요! 오늘의 마음을 **감정 일기**에 남겨보세요.")

    st.markdown("---")
    st.markdown(
        """
**이 앱으로 할 수 있는 것**
- 📋 나의 스트레스 정도 확인하기
- 🫁 호흡으로 몸과 마음 진정시키기
- 💡 상황별 스트레스 대처 방법 알아보기
- 📝 감정 일기 쓰고 저장하기
"""
    )

# ---------------- 스트레스 체크 ----------------
elif menu == "📋 스트레스 체크":
    st.title("📋 스트레스 자가 체크")
    st.caption("최근 2주 동안의 나를 떠올리며 답해보세요. (진단 도구가 아닌 자기 점검용입니다)")

    questions = [
        "공부나 시험 때문에 부담감을 느낀다.",
        "잠들기 어렵거나 자고 나도 피곤하다.",
        "작은 일에도 짜증이 나거나 예민해진다.",
        "친구 관계 때문에 신경 쓰이는 일이 있다.",
        "집중이 잘 안 되고 멍할 때가 많다.",
        "머리나 배가 아프거나 몸이 무겁다.",
        "하고 싶은 일이 없고 의욕이 떨어진다.",
        "미래(진로, 성적)에 대해 걱정이 많다.",
    ]
    options = {"전혀 아니다": 0, "가끔 그렇다": 1, "자주 그렇다": 2, "거의 항상 그렇다": 3}

    with st.form("stress_form"):
        answers = []
        for i, q in enumerate(questions, 1):
            a = st.radio(f"{i}. {q}", list(options.keys()), horizontal=True, key=f"q{i}")
            answers.append(options[a])
        submitted = st.form_submit_button("결과 보기")

    if submitted:
        score = sum(answers)
        max_score = len(questions) * 3
        st.progress(score / max_score)
        st.metric("나의 점수", f"{score} / {max_score}")

        if score <= 8:
            st.success("🟢 **낮음** — 스트레스를 잘 관리하고 있어요. 지금의 생활 습관을 유지해보세요!")
        elif score <= 16:
            st.warning("🟡 **보통** — 어느 정도 스트레스가 쌓여 있어요. 호흡 연습과 대처 방법을 활용해보세요.")
        else:
            st.error(
                "🔴 **높음** — 요즘 많이 힘들었겠어요. 혼자 견디지 말고 담임선생님, "
                "Wee클래스 상담선생님, 보호자에게 꼭 이야기해보세요. **📞 도움 받기** 메뉴도 확인해주세요."
            )

# ---------------- 호흡 연습 ----------------
elif menu == "🫁 호흡 연습":
    st.title("🫁 4-4-4 박스 호흡")
    st.write("숨을 **4초 들이쉬고 → 4초 멈추고 → 4초 내쉬는** 호흡이에요. 긴장을 푸는 데 도움이 돼요.")

    rounds = st.slider("몇 번 반복할까요?", 1, 8, 4)

    if st.button("▶ 시작하기"):
        guide = st.empty()
        bar = st.progress(0)
        steps = [("🌬️ 들이쉬기", "코로 천천히"), ("⏸️ 멈추기", "편안하게 참기"), ("😮‍💨 내쉬기", "입으로 길게")]
        for r in range(rounds):
            for title, desc in steps:
                for sec in range(4, 0, -1):
                    guide.markdown(
                        f"<h2 style='text-align:center'>{title}</h2>"
                        f"<h1 style='text-align:center'>{sec}</h1>"
                        f"<p style='text-align:center'>{desc} · {r + 1}/{rounds}회</p>",
                        unsafe_allow_html=True,
                    )
                    time.sleep(1)
            bar.progress((r + 1) / rounds)
        guide.markdown("<h2 style='text-align:center'>✨ 잘했어요!</h2>", unsafe_allow_html=True)
        st.balloons()

# ---------------- 대처 방법 ----------------
elif menu == "💡 대처 방법":
    st.title("💡 상황별 대처 방법")

    tips = {
        "📚 시험·성적 스트레스": [
            "큰 목표를 오늘 할 수 있는 작은 목표로 쪼개기",
            "25분 공부 + 5분 휴식(뽀모도로) 해보기",
            "결과보다 '오늘 내가 한 노력'을 기록하기",
        ],
        "👥 친구 관계 스트레스": [
            "내 감정을 '나는 ~해서 속상했어'로 표현해보기",
            "모든 친구와 다 잘 지내지 않아도 괜찮다고 생각하기",
            "믿을 수 있는 사람 한 명에게 털어놓기",
        ],
        "🏠 가족 관계 스트레스": [
            "감정이 격할 때는 잠시 자리를 피했다가 다시 대화하기",
            "하고 싶은 말을 미리 메모로 정리해보기",
            "상담선생님에게 도움 요청하기",
        ],
        "😴 잠·생활 리듬": [
            "자기 30분 전에는 스마트폰 내려놓기",
            "매일 비슷한 시간에 자고 일어나기",
            "낮에 햇빛 보며 10분 걷기",
        ],
        "🔮 진로·미래 걱정": [
            "걱정을 종이에 적고 '지금 할 수 있는 것'에 동그라미 치기",
            "관심 있는 분야를 하나 정해 영상·책으로 탐색해보기",
            "고1은 탐색하는 시기라는 것 기억하기",
        ],
    }

    for situation, items in tips.items():
        with st.expander(situation):
            for t in items:
                st.markdown(f"- {t}")

    st.markdown("---")
    st.subheader("🎲 오늘의 마음 미션")
    missions = [
        "좋아하는 노래 한 곡 끝까지 듣기",
        "오늘 감사한 일 3가지 적기",
        "친구에게 고마운 점 한 가지 말하기",
        "10분 동안 산책하기",
        "물 한 잔 천천히 마시기",
        "스트레칭 5분 하기",
        "나에게 칭찬 한 마디 해주기",
    ]
    if st.button("미션 뽑기"):
        st.success(f"🎯 {missions[int(time.time()) % len(missions)]}")

# ---------------- 감정 일기 ----------------
elif menu == "📝 감정 일기":
    st.title("📝 감정 일기")
    st.caption("작성한 일기는 이 화면을 닫으면 사라져요. 저장하려면 아래 다운로드 버튼을 눌러주세요.")

    with st.form("journal_form", clear_on_submit=True):
        emotion = st.selectbox("지금 느끼는 감정", ["기쁨", "편안함", "걱정", "불안", "슬픔", "화남", "지침", "기타"])
        level = st.slider("감정의 세기", 1, 10, 5)
        reason = st.text_area("어떤 일이 있었나요?")
        good = st.text_input("그래도 오늘 좋았던 점 한 가지")
        if st.form_submit_button("기록하기"):
            st.session_state.journal.append(
                {
                    "날짜": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "감정": emotion,
                    "세기": level,
                    "있었던 일": reason,
                    "좋았던 점": good,
                }
            )
            st.success("기록했어요! 마음을 들여다본 것만으로도 잘한 거예요. 🌱")

    if st.session_state.journal:
        df = pd.DataFrame(st.session_state.journal)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.bar_chart(df["감정"].value_counts())
        st.download_button(
            "💾 일기 다운로드 (CSV)",
            df.to_csv(index=False).encode("utf-8-sig"),
            file_name="감정일기.csv",
            mime="text/csv",
        )

# ---------------- 도움 받기 ----------------
elif menu == "📞 도움 받기":
    st.title("📞 도움이 필요할 때")
    st.write("힘든 마음을 이야기하는 건 약한 게 아니라 **용기 있는 행동**이에요.")

    st.markdown(
        """
**학교 안에서**
- 담임선생님
- Wee클래스 상담선생님
- 보건선생님

**학교 밖에서 (24시간)**
- 📞 **청소년상담전화 1388** (문자: #1388, 카카오톡: '청소년상담1388')
- 📞 **자살예방상담전화 109**
- 📞 **정신건강위기상담 1577-0199**
"""
    )
    st.error("🚨 지금 당장 위험하다고 느껴지면 **112** 또는 **119**에 바로 연락하세요.")
