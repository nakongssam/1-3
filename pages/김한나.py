import datetime
import streamlit as st

# 1. 페이지 설정 및 테마
st.set_page_config(
    page_title="스마트 시험 디데이 플래너", page_icon="📅", layout="centered"
)

# 2. 세션 상태(Session State) 초기화 (앱이 새로고침되어도 데이터 유지)
if "tasks" not in st.st:
    st.session_state.tasks = [
        {"subject": "국어", "plan": "교과서 3회독 및 기출문제 풀이", "done": False},
        {"subject": "수학", "plan": "쎈 C단계 오답노트 정리", "done": False},
        {"subject": "기술가정", "plan": "프린트물 개념 암기", "done": False},
    ]

if "motto" not in st.session_state:
    st.session_state.motto = "끝까지 포기하지 말고 최선을 다하자!"

# 3. 사이드바: 시험 정보 설정
st.sidebar.header("⚙️ 시험 일정 설정")
exam_name = st.sidebar.text_input(
    "시험 명칭", value="2026년 1학기 지필평가", max_chars=20
)
exam_date = st.sidebar.date_input("시험 시작일", value=datetime.date.today() + datetime.timedelta(days=14))

# 4. 메인 화면: 타이틀 및 디데이 계산
st.title("📅 스마트 시험 디데이 플래너")
st.markdown("---")

# 날짜 계산 및 예외 처리
today = datetime.date.today()
delta = exam_date - today
d_day = delta.days

# 디데이 표시 및 맞춤형 메시지
if d_day > 0:
    st.metric(label=f"🔥 {exam_name}까지", value=f"D-{d_day}")

    # 남은 기간별 동기부여 메시지 차별화
    if d_day >= 14:
        st.info(f"💡 {st.session_state.motto} \n\n(아직 여유가 있습니다! 기초 개념을 탄탄히 다질 때입니다.)")
    elif 7 <= d_day < 14:
        st.warning(
            f"⚡ {st.session_state.motto} \n\n(시험이 일주일 앞으로 다가왔습니다. 취약한 단원을 집중 보완하세요!)"
        )
    else:
        st.error(
            f"🚨 {st.session_state.motto} \n\n(컨디션 관리가 중요한 시기입니다. 오답 노트 위주로 마무리하세요!)"
        )

    # 시각적 진행바 (최대 30일 기준으로 대략적인 진행률 표시)
    progress_percent = max(0, min(100, int((30 - d_day) / 30 * 100))) if d_day < 30 else 0
    st.caption("시험 준비 진행도 (30일 기준 계산)")
    st.progress(progress_percent)

elif d_day == 0:
    st.success(f"🎉 드디어 시험 당일입니다! {st.session_state.motto} 실력 발휘 제대로 하고 오세요!")
    st.balloons()
else:
    st.subheader(f"🏁 {exam_name}이 종료되었습니다.")
    st.info("시험 보느라 모두 고생 많으셨습니다! 달콤한 휴식을 즐기세요. 👏")

st.markdown("---")

# 5. 메인 기능 1: 오늘의 다짐 한 줄 변경
st.subheader("✍️ 오늘의 한 줄 다짐")
new_motto = st.text_input("나에게 자극이 되는 한 마디를 적어보세요:", value=st.session_state.motto)
if new_motto != st.session_state.motto:
    st.session_state.motto = new_motto
    st.rerun()

st.markdown("---")

# 6. 메인 기능 2: 과목별 목표 및 체크리스트 (플래너)
st.subheader("📝 과목별 공부 계획 & 체크리스트")

# 새로운 계획 추가 양식
with st.form(key="todo_form", clear_on_submit=True):
    col1, col2 = st.columns([1, 2])
    with col1:
        new_subject = st.text_input("과목명", placeholder="예: 영어")
    with col2:
        new_plan = st.text_input("공부 계획", placeholder="예: 단어장 1~5과 암기")

    submit_button = st.form_submit_with_ Garner = st.form_submit_button(
        label="계획 추가"
    )

    if submit_button:
        if new_subject.strip() and new_plan.strip():
            st.session_state.tasks.append(
                {"subject": new_subject, "plan": new_plan, "done": False}
            )
            st.rerun()
        else:
            st.error("과목명과 공부 계획을 모두 입력해주세요.")

# 등록된 계획 리스트 출력 (체크박스 구현)
if st.session_state.tasks:
    st.write("### 나의 대시보드")
    completed_count = 0

    for idx, task in enumerate(st.session_state.tasks):
        # 체크박스 상태 변경 시 세션 상태에 즉시 반영
        # 중복 key 방지를 위해 idx 활용
        is_done = st.checkbox(
            f"**[{task['subject']}]** {task['plan']}",
            value=task["done"],
            key=f"task_{idx}",
        )

        if is_done:
            completed_count += 1
        st.session_state.tasks[idx]["done"] = is_done

    # 달성률 표시
    total_tasks = len(st.session_state.tasks)
    achievement_rate = int((completed_count / total_tasks) * 100)
    st.write(f"📊 **현재 계획 달성률:** {achievement_rate}% ({completed_count}/{total_tasks})")

    # 전체 초기화 버튼
    if st.button("계획 전체 삭제하기"):
        st.session_state.tasks = []
        st.rerun()
else:
    st.info("등록된 공부 계획이 없습니다. 위의 양식에서 시험 계획을 추가해보세요!")
