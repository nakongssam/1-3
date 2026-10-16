
import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="마음 쉼터", page_icon="🌿")

st.title("🌿 마음 쉼터")
st.write("오늘의 스트레스를 가볍게 관리해 보세요!")

# 기록 저장 (현재 접속 세션 동안 유지)
if "records" not in st.session_state:
    st.session_state.records = []

st.subheader("😊 오늘의 기분은?")

score = st.slider("스트레스 점수를 선택하세요", 0, 10, 5)

reason = st.selectbox(
    "스트레스의 원인은 무엇인가요?",
    ["공부", "친구", "가족", "연애", "진로", "기타"]
)

memo = st.text_input("오늘의 마음을 한 줄로 적어보세요.")

if st.button("💾 오늘의 마음 기록하기"):
    st.session_state.records.append({
        "시간": datetime.now().strftime("%H:%M:%S"),
        "스트레스": score,
        "원인": reason,
        "메모": memo
    })
    st.success("오늘의 마음을 기록했어요!")

st.divider()

st.subheader("💌 마음을 위한 조언")

if score <= 3:
    st.success("마음이 비교적 편안하네요! 지금의 여유를 즐겨보세요.")
elif score <= 6:
    st.info("조금 지쳤나요? 잠시 쉬면서 좋아하는 음악을 들어보세요.")
else:
    st.warning("스트레스가 높네요. 잠시 쉬고 믿을 만한 사람과 이야기해 보세요.")

st.divider()

st.subheader("🧘 1분 호흡 운동")
st.write("천천히 따라 해보세요.")

if st.button("호흡 운동 시작"):
    st.info("4초 동안 숨을 들이마시고, 6초 동안 내쉬세요.")
    st.write("이 과정을 6번 반복해 보세요. 🌸")

st.divider()

st.subheader("📊 나의 스트레스 기록")

if st.session_state.records:
    df = pd.DataFrame(st.session_state.records)
    st.line_chart(df["스트레스"])
    st.dataframe(df, use_container_width=True)
else:
    st.write("아직 기록이 없어요.")

st.caption("🌱 하루하루 나의 마음을 돌보는 작은 습관")
