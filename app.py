```python
import streamlit as st
from datetime import date

# 기본 설정
st.set_page_config(
    page_title="스케줄 관리",
    page_icon="📅",
    layout="centered"
)

# 세션 상태 저장
if "schedules" not in st.session_state:
    st.session_state.schedules = []

# 스타일
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

.date {
    color: gray;
    font-size: 14px;
}

.task {
    font-size: 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<div class="title">📅 스케줄 관리</div>', unsafe_allow_html=True)

# 입력창
with st.container():
    col1, col2 = st.columns([1, 2])

    with col1:
        selected_date = st.date_input("날짜", value=date.today())

    with col2:
        task = st.text_input("할 일 입력")

# 추가 버튼
if st.button("추가하기", use_container_width=True):

    if task.strip() != "":
        st.session_state.schedules.append({
            "date": selected_date.strftime("%Y-%m-%d"),
            "task": task
        })
        st.success("추가 완료!")
    else:
        st.warning("할 일을 입력해주세요.")

st.markdown("## 📌 일정 목록")

# 일정 출력
if len(st.session_state.schedules) == 0:
    st.info("등록된 일정이 없습니다.")

else:
    for item in reversed(st.session_state.schedules):

        st.markdown(f"""
        <div class="card">
            <div class="date">{item['date']}</div>
            <div class="task">{item['task']}</div>
        </div>
        """, unsafe_allow_html=True)

# 전체 삭제
if len(st.session_state.schedules) > 0:
    if st.button("전체 삭제"):
        st.session_state.schedules = []
        st.rerun()
```
