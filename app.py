
import streamlit as st
import random
import csv
import io
from datetime import date, datetime, timedelta

st.set_page_config(
    page_title="스터디 메이트",
    page_icon="📚",
    layout="wide"
)

# 화면 디자인
st.markdown("""
<style>
.block-container {max-width: 1000px; padding-top: 2rem;}
h1, h2, h3 {color: #355c7d;}
div.stButton > button {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

SUBJECTS = [
    "국어", "영어", "수학", "통합과학",
    "통합사회", "한국사", "정보", "기타"
]

MESSAGES = [
    "오늘의 작은 노력이 내일의 실력이 됩니다! 🌱",
    "완벽하지 않아도 괜찮아요. 꾸준함이 중요해요!",
    "딱 25분만 집중해 볼까요? 🔥",
    "어제보다 조금만 성장해도 성공이에요!",
    "쉬는 것도 공부의 일부입니다. ☕",
    "지금 시작하는 사람이 결국 해냅니다!"
]

# 세션 데이터 초기화
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "records" not in st.session_state:
    st.session_state.records = []

if "timer_end" not in st.session_state:
    st.session_state.timer_end = None

if "timer_subject" not in st.session_state:
    st.session_state.timer_subject = "수학"

if "timer_minutes" not in st.session_state:
    st.session_state.timer_minutes = 25

if "timer_mode" not in st.session_state:
    st.session_state.timer_mode = "집중"

if "message" not in st.session_state:
    st.session_state.message = random.choice(MESSAGES)


def add_record(subject, minutes):
    """공부 기록 추가"""
    if minutes <= 0:
        return

    st.session_state.records.append({
        "날짜": date.today().isoformat(),
        "과목": subject,
        "공부시간(분)": int(minutes)
    })


def make_csv(rows, columns):
    """CSV 다운로드 데이터 생성"""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")


# 상단 화면
st.title("📚 스터디 메이트")
st.caption("공부 계획부터 집중 시간까지, 나만의 학습 관리 공간")

st.info(st.session_state.message)

if st.button("✨ 새로운 응원 메시지"):
    st.session_state.message = random.choice(MESSAGES)
    st.rerun()

# 오늘의 통계
today = date.today().isoformat()

today_records = [
    r for r in st.session_state.records
    if r["날짜"] == today
]

today_minutes = sum(
    r["공부시간(분)"] for r in today_records
)

today_tasks = [
    t for t in st.session_state.tasks
    if t["날짜"] == today
]

completed = sum(t["완료"] for t in today_tasks)
total_tasks = len(today_tasks)

col1, col2, col3 = st.columns(3)

col1.metric("⏱️ 오늘 공부", f"{today_minutes}분")
col2.metric("✅ 완료한 계획", f"{completed}/{total_tasks}")
col3.metric(
    "🎯 목표 달성률",
    f"{completed / total_tasks * 100:.0f}%"
    if total_tasks else "0%"
)

st.divider()

tab1, tab2, tab3 = st.tabs([
    "📝 공부 계획",
    "⏰ 집중 타이머",
    "📊 공부 통계"
])

# -------------------------
# 1. 공부 계획
# -------------------------
with tab1:
    st.subheader("오늘의 공부 계획")

    with st.form("add_task", clear_on_submit=True):
        subject = st.selectbox("과목 선택", SUBJECTS)
        task_text = st.text_input(
            "공부할 내용",
            placeholder="예: 수학 문제집 20문제 풀기"
        )
        goal = st.number_input(
            "목표 공부 시간(분)",
            min_value=5,
            max_value=600,
            value=30,
            step=5
        )

        submitted = st.form_submit_button(
            "➕ 계획 추가",
            use_container_width=True
        )

        if submitted:
            if not task_text.strip():
                st.warning("공부할 내용을 입력해 주세요.")
            else:
                st.session_state.tasks.append({
                    "날짜": today,
                    "과목": subject,
                    "내용": task_text.strip(),
                    "목표시간": int(goal),
                    "완료": False
                })
                st.success("공부 계획이 추가되었습니다!")
                st.rerun()

    st.divider()

    st.markdown("#### 📋 오늘의 할 일")

    if not today_tasks:
        st.info("아직 공부 계획이 없어요. 첫 계획을 추가해 보세요!")

    for i, task in enumerate(st.session_state.tasks):
        if task["날짜"] != today:
            continue

        c1, c2 = st.columns([5, 1])

        with c1:
            checked = st.checkbox(
                f"{task['과목']} | {task['내용']} "
                f"({task['목표시간']}분)",
                value=task["완료"],
                key=f"task_{i}"
            )
            st.session_state.tasks[i]["완료"] = checked

        with c2:
            if st.button("삭제", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

    st.divider()

    total_goal = sum(t["목표시간"] for t in today_tasks)
    st.write(f"📌 오늘의 목표 공부 시간: **{total_goal}분**")

    if total_goal > 0:
        st.progress(min(today_minutes / total_goal, 1.0))

# -------------------------
# 2. 집중 타이머
# -------------------------
with tab2:
    st.subheader("⏰ 집중 타이머")
    st.write("공부 시간을 정하고 집중해 보세요!")

    mode = st.radio(
        "모드 선택",
        ["집중", "휴식"],
        horizontal=True,
        disabled=st.session_state.timer_end is not None
    )

    timer_subject = st.selectbox(
        "공부할 과목",
        SUBJECTS,
        disabled=st.session_state.timer_end is not None
    )

    default_time = 25 if mode == "집중" else 5

    minutes = st.number_input(
        "타이머 시간(분)",
        min_value=1,
        max_value=180,
        value=default_time,
        disabled=st.session_state.timer_end is not None
    )

    if st.session_state.timer_end is None:
        if st.button(
            "▶️ 타이머 시작",
            use_container_width=True
        ):
            st.session_state.timer_end = (
                datetime.now() + timedelta(minutes=minutes)
            )
            st.session_state.timer_subject = timer_subject
            st.session_state.timer_minutes = minutes
            st.session_state.timer_mode = mode
            st.rerun()

    else:
        remaining = (
            st.session_state.timer_end - datetime.now()
        ).total_seconds()

        if remaining > 0:
            seconds = max(0, int(remaining))
            mm, ss = divmod(seconds, 60)

            st.markdown(
                f"## ⏳ {mm:02d}:{ss:02d}"
            )
            st.progress(
                max(
                    0.0,
                    min(
                        remaining /
                        (st.session_state.timer_minutes * 60),
                        1.0
                    )
                )
            )

            st.caption(
                "시간 표시를 갱신하려면 아래 버튼을 눌러주세요."
            )

            if st.button("🔄 남은 시간 새로고침"):
                st.rerun()

            if st.button("⏹️ 타이머 취소"):
                st.session_state.timer_end = None
                st.rerun()

        else:
            st.success("🎉 타이머가 완료되었습니다!")
            st.balloons()

            if st.session_state.timer_mode == "집중":
                add_record(
                    st.session_state.timer_subject,
                    st.session_state.timer_minutes
                )
                st.success("공부 시간이 자동 기록되었습니다!")

            st.session_state.timer_end = None
            st.rerun()

    st.caption(
        "※ 타이머는 화면을 새로고침할 때 시간이 갱신됩니다. "
        "종료 후 앱을 다시 열어야 완료 기록이 반영됩니다."
    )

    st.divider()

    st.markdown("#### ✍️ 공부 시간 직접 기록")

    with st.form("manual_record"):
        record_subject = st.selectbox(
            "과목",
            SUBJECTS,
            key="manual_subject"
        )
        record_minutes = st.number_input(
            "공부한 시간(분)",
            min_value=1,
            max_value=600,
            value=30
        )

        if st.form_submit_button("💾 공부 기록 저장"):
            add_record(record_subject, record_minutes)
            st.success("공부 시간이 저장되었습니다!")
            st.rerun()

# -------------------------
# 3. 공부 통계
# -------------------------
with tab3:
    st.subheader("📊 나의 공부 통계")

    records = st.session_state.records

    if not records:
        st.info("아직 공부 기록이 없습니다.")
    else:
        total = sum(r["공부시간(분)"] for r in records)

        st.metric(
            "누적 공부 시간",
            f"{total // 60}시간 {total % 60}분"
        )

        subject_totals = {}

        for record in records:
            subject = record["과목"]
            subject_totals[subject] = (
                subject_totals.get(subject, 0)
                + record["공부시간(분)"]
            )

        st.markdown("#### 📚 과목별 공부 시간")
        st.bar_chart(subject_totals)

        st.markdown("#### 📅 날짜별 공부 시간")

        daily_totals = {}

        for record in records:
            day = record["날짜"]
            daily_totals[day] = (
                daily_totals.get(day, 0)
                + record["공부시간(분)"]
            )

        st.line_chart(dict(sorted(daily_totals.items())))

        st.markdown("#### 📋 상세 공부 기록")
        st.dataframe(
            records,
            use_container_width=True,
            hide_index=True
        )

        csv_data = make_csv(
            records,
            ["날짜", "과목", "공부시간(분)"]
        )

        st.download_button(
            "📥 공부 기록 CSV 다운로드",
            data=csv_data,
            file_name="study_records.csv",
            mime="text/csv",
            use_container_width=True
        )

        if st.button("🗑️ 공부 기록 전체 삭제"):
            st.session_state.records = []
            st.rerun()

st.divider()
st.caption(
    "📚 Study Mate | 나의 성장을 기록하는 공부 앱"
)
