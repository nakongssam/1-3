
import streamlit as st
import random

st.set_page_config(page_title="오늘 뭐 먹지?", page_icon="🍱")

st.title("🍱 오늘 뭐 먹지?")
st.write("메뉴 고민은 이제 그만!")

foods = {
    "한식": ["김치찌개", "제육볶음", "비빔밥", "삼겹살"],
    "중식": ["마라탕", "짜장면", "짬뽕", "탕수육"],
    "일식": ["초밥", "라멘", "돈가스", "우동"],
    "양식": ["피자", "파스타", "햄버거", "스테이크"]
}

category = st.selectbox("음식 종류를 선택하세요", list(foods.keys()))

if st.button("🎲 메뉴 추천받기"):
    food = random.choice(foods[category])
    st.success(f"오늘의 추천 메뉴는 {food}!")
    if food == "마라탕":
        st.balloons()
        st.write("🌶️ 마라탕 당첨! 맛있게 먹어요!")

st.divider()
st.caption("Made with Streamlit")
