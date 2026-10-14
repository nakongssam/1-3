
import streamlit as st
import random

st.set_page_config(
    page_title="고1 LIFE LAB",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 고1 LIFE LAB")
st.caption("고등학교 1학년을 위한 재미있는 학교생활 앱")

menu = st.sidebar.radio(
    "메뉴 선택",
    ["🏠 홈", "🎯 진로 유형 테스트", "⚖️ 밸런스 게임", "🍱 메뉴 추천"]
)

if menu == "🏠 홈":
    st.header("반가워요! 👋")
    st.write("고등학교 생활, 조금 더 재미있게 즐겨볼까요?")
    st.info("왼쪽 메뉴에서 원하는 활동을 선택하세요!")

    st.subheader("오늘의 응원 한마디")
    messages = [
        "오늘도 충분히 잘하고 있어!",
        "실수해도 괜찮아. 배우는 중이니까!",
        "남과 비교하지 말고 어제의 나와 비교하자!",
        "작은 도전이 큰 변화를 만든다!"
    ]

    if st.button("응원 메시지 받기"):
        st.success(random.choice(messages))

elif menu == "🎯 진로 유형 테스트":
    st.header("🎯 나의 진로 유형 찾기")
    st.write("질문에 답하고 나에게 어울리는 진로를 찾아보세요.")

    questions = [
        "새로운 기계를 만들거나 작동시키는 일이 재미있다.",
        "친구의 고민을 듣고 도와주는 것이 좋다.",
        "그림을 그리거나 새로운 디자인을 만드는 것이 좋다.",
        "숫자나 자료를 분석하는 것이 재미있다.",
        "컴퓨터 프로그램이나 AI에 관심이 많다.",
        "사람들 앞에서 발표하거나 설명하는 것이 좋다.",
        "영상, 음악, 콘텐츠를 만드는 것이 재미있다.",
        "과학 실험이나 문제 해결 활동이 좋다."
    ]

    categories = [
        "기술·공학", "사회·교육", "예술·디자인", "연구·분석",
        "기술·공학", "사회·교육", "예술·디자인", "연구·분석"
    ]

    scores = {
        "기술·공학": 0,
        "사회·교육": 0,
        "예술·디자인": 0,
        "연구·분석": 0
    }

    with st.form("career_test"):
        answers = []

        for i, question in enumerate(questions):
            answer = st.radio(
                f"Q{i+1}. {question}",
                ["전혀 아니다", "아니다", "보통", "그렇다", "매우 그렇다"],
                index=2,
                key=f"q{i}"
            )
            answers.append(answer)

        submitted = st.form_submit_button("결과 확인하기")

    if submitted:
        points = {
            "전혀 아니다": 1,
            "아니다": 2,
            "보통": 3,
            "그렇다": 4,
            "매우 그렇다": 5
        }

        for category, answer in zip(categories, answers):
            scores[category] += points[answer]

        best = max(scores, key=scores.get)

        careers = {
            "기술·공학": ["소프트웨어 개발자", "AI 엔지니어", "로봇공학자"],
            "사회·교육": ["교사", "상담사", "사회복지사"],
            "예술·디자인": ["디자이너", "영상 제작자", "콘텐츠 기획자"],
            "연구·분석": ["과학자", "데이터 분석가", "연구원"]
        }

        st.success(f"당신의 관심 유형은 {best} 분야!")
        st.subheader("추천 직업")

        for career in careers[best]:
            st.write("✅", career)

        st.subheader("분야별 관심 점수")
        st.bar_chart(scores)

        st.caption(
            "이 결과는 흥미 탐색용이며, 실제 적성이나 진로를 확정하지 않습니다."
        )

elif menu == "⚖️ 밸런스 게임":
    st.header("⚖️ 고1 밸런스 게임")

    games = [
        ("시험 하루 전 모든 내용 암기하기", "수행평가 항상 만점 받기"),
        ("매일 1교시 체육", "매일 마지막 교시 자습"),
        ("급식 메뉴 매일 내가 정하기", "학교 시간표 매일 내가 정하기"),
        ("친구들과 수학여행 3박 4일", "친구들과 놀이공원 3번"),
        ("모든 과목 숙제 없음", "모든 과목 시험 없음"),
        ("한 달 동안 스마트폰 없이 살기", "한 달 동안 게임 없이 살기")
    ]

    if "game_index" not in st.session_state:
        st.session_state.game_index = 0

    a, b = games[st.session_state.game_index]

    st.subheader("둘 중 하나만 선택한다면?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"🅰️ {a}", use_container_width=True):
            st.success(f"선택: {a}")

    with col2:
        if st.button(f"🅱️ {b}", use_container_width=True):
            st.success(f"선택: {b}")

    if st.button("🔄 다음 질문"):
        st.session_state.game_index = (
            st.session_state.game_index + 1
        ) % len(games)
        st.rerun()

elif menu == "🍱 메뉴 추천":
    st.header("🍱 오늘 뭐 먹지?")
    st.write("메뉴 고민은 이제 그만!")

    food = {
        "한식": ["김치찌개", "비빔밥", "제육덮밥", "불고기", "칼국수"],
        "중식": ["짜장면", "짬뽕", "볶음밥", "마파두부덮밥"],
        "일식": ["돈가스", "우동", "초밥", "규동"],
        "양식": ["파스타", "피자", "햄버거", "리조또"],
        "분식": ["떡볶이", "김밥", "라면", "순대"]
    }

    category = st.selectbox(
        "어떤 종류가 좋아?",
        ["전체"] + list(food.keys())
    )

    if st.button("🎲 메뉴 뽑기"):
        if category == "전체":
            candidates = [
                item for items in food.values() for item in items
            ]
        else:
            candidates = food[category]

        st.success(f"오늘의 추천 메뉴는 {random.choice(candidates)}!")
        st.balloons()

st.divider()
st.caption("Made for High School Students | 고1 LIFE LAB")
