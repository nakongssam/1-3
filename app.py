
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="급식 알리미",
    page_icon="🍜",
    layout="centered"
)

st.title("🍜 오늘 급식 뭐야?")
st.caption("마라탕 나오는 날은 절대 놓치지 말자!")

# 기본 급식표 (예시 데이터)
DEFAULT_MEALS = {
    "월요일": "쌀밥, 미역국, 제육볶음, 김치",
    "화요일": "마라탕, 꿔바로우, 단무지",
    "수요일": "치킨마요덮밥, 떡볶이, 요구르트",
    "목요일": "카레라이스, 돈까스, 샐러드",
    "금요일": "마라샹궈, 볶음밥, 탕후루"
}

if "meals" not in st.session_state:
    st.session_state.meals = DEFAULT_MEALS.copy()

days = list(DEFAULT_MEALS.keys())

# 취향 설정
st.sidebar.header("❤️ 나의 음식 취향")

favorites_text = st.sidebar.text_input(
    "좋아하는 음식",
    "마라탕, 마라샹궈, 떡볶이, 치킨, 돈까스"
)

favorites = [
    x.strip().lower()
    for x in favorites_text.split(",")
    if x.strip()
]

st.sidebar.info("🔥 마라탕을 좋아하는 사람을 위한 급식 탐지기!")

# 급식표 수정
with st.expander("✏️ 이번 주 급식표 입력 / 수정"):
    with st.form("meal_form"):
        new_meals = {}

        for day in days:
            new_meals[day] = st.text_input(
                day,
                value=st.session_state.meals[day]
            )

        submitted = st.form_submit_button(
            "💾 급식표 저장",
            use_container_width=True
        )

        if submitted:
            st.session_state.meals = new_meals
            st.success("급식표가 저장되었어요!")

# 취향 점수 계산
def calculate_score(menu):
    text = menu.lower()
    matched = [food for food in favorites if food in text]

    score = min(100, 50 + len(matched) * 25)
    return score, matched

tab1, tab2, tab3 = st.tabs([
    "🍱 급식표",
    "🔥 마라 탐지기",
    "🏆 급식 랭킹"
])

with tab1:
    st.subheader("📅 이번 주 급식")

    selected_day = st.selectbox("요일 선택", days)
    menu = st.session_state.meals[selected_day]

    score, matched = calculate_score(menu)

    st.metric("💖 취향 저격 점수", f"{score}점")

    if "마라" in menu:
        st.success("🔥 대박! 마라 메뉴가 나오는 날!")
        st.balloons()
    elif matched:
        st.success("😍 좋아하는 음식이 있어요!")
    else:
        st.info("🍚 오늘은 평범한 급식 데이!")

    st.markdown("### 🍽️ 오늘의 메뉴")

    for food in menu.split(","):
        food = food.strip()
        if not food:
            continue
        if any(f in food.lower() for f in favorites):
            st.markdown(f"**❤️ {food}**")
        else:
            st.write(f"🍴 {food}")

with tab2:
    st.subheader("🔥 마라탕 탐지기")

    found = []

    for day, menu in st.session_state.meals.items():
        if "마라" in menu:
            found.append((day, menu))

    if found:
        st.success(f"🎉 마라 메뉴가 {len(found)}일 나와요!")

        for day, menu in found:
            st.markdown(f"### 🔥 {day}")
            st.write(menu)
    else:
        st.warning("😭 이번 주에는 마라 메뉴가 없어요!")

with tab3:
    st.subheader("🏆 이번 주 급식 랭킹")

    ranking = []

    for day, menu in st.session_state.meals.items():
        score, matched = calculate_score(menu)
        ranking.append((day, score, menu))

    ranking.sort(key=lambda x: x[1], reverse=True)

    for rank, (day, score, menu) in enumerate(ranking, 1):
        if rank == 1:
            st.markdown(f"### 🥇 {day} — {score}점")
        elif rank == 2:
            st.markdown(f"### 🥈 {day} — {score}점")
        elif rank == 3:
            st.markdown(f"### 🥉 {day} — {score}점")
        else:
            st.markdown(f"**{rank}위. {day} — {score}점**")

        st.caption(menu)

st.divider()
st.caption("🍜 급식 알리미 | 마라탕은 사랑입니다 ❤️")
