
import streamlit as st
from datetime import datetime
from urllib.parse import quote
import html

st.set_page_config(
    page_title="안심지하철 | 보호자 연락",
    page_icon="🚇",
    layout="centered"
)

# 이동 정보 저장
defaults = {
    "stage": 0,
    "start": "천안역",
    "end": "서울역",
    "guardian": "",
    "phone": "",
    "departed_at": "",
    "arrived_at": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 핑크 디자인
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        160deg, #fff9fc, #ffe1ee, #ffd1e3
    );
}
.block-container {
    max-width: 590px;
    padding-top: 1.5rem;
}
.hero {
    background: linear-gradient(125deg, #f4258d, #fa7091);
    color: white;
    border-radius: 28px;
    padding: 28px 25px;
    margin-bottom: 22px;
    box-shadow: 0 12px 25px #e83b7d30;
}
.hero h1 {
    color: white;
    font-size: 2.1rem;
}
.hero p {
    color: white;
}
.info {
    background: #ffffffdd;
    border-radius: 22px;
    padding: 22px;
    margin: 15px 0;
}
.big {
    font-size: 1.4rem;
    font-weight: 800;
    color: #e82482;
}
.status {
    text-align: center;
    background: white;
    border-radius: 22px;
    padding: 30px;
    margin: 18px 0;
}
.stButton > button {
    width: 100%;
    min-height: 58px;
    border-radius: 30px;
    font-size: 1.1rem;
    font-weight: bold;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #ef258d, #fa6d8a);
    color: white;
    border: none;
}
.stTextInput input {
    border-radius: 14px;
    min-height: 48px;
}
a.sms {
    display: block;
    text-align: center;
    background: linear-gradient(90deg, #f0258b, #fa6d8a);
    color: white !important;
    padding: 20px;
    border-radius: 30px;
    text-decoration: none;
    font-size: 1.15rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div>🚇 SAFE METRO</div>
    <h1>안심지하철 💗</h1>
    <p>어르신의 안전한 이동, 보호자와 함께해요.</p>
</div>
""", unsafe_allow_html=True)

stage = st.session_state.stage

# 1단계: 이동 계획
if stage == 0:
    st.subheader("📍 이동 계획 설정")

    st.text_input("출발역", key="start")
    st.text_input("도착역", key="end")

    st.subheader("👨‍👩‍👧 보호자 정보")

    st.text_input(
        "보호자 이름",
        key="guardian",
        placeholder="예: 김보호"
    )
    st.text_input(
        "보호자 전화번호",
        key="phone",
        placeholder="01012345678"
    )

    if st.button("🚇 이동 시작하기", type="primary"):
        phone = st.session_state.phone.replace("-", "").replace(" ", "")

        if not st.session_state.start.strip() or not st.session_state.end.strip():
            st.error("출발역과 도착역을 입력해 주세요.")
        elif st.session_state.start.strip() == st.session_state.end.strip():
            st.error("출발역과 도착역을 다르게 입력해 주세요.")
        elif not st.session_state.guardian.strip():
            st.error("보호자 이름을 입력해 주세요.")
        elif not (phone.isdigit() and len(phone) in (10, 11)):
            st.error("전화번호를 정확히 입력해 주세요.")
        else:
            st.session_state.departed_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            )
            st.session_state.stage = 1
            st.rerun()

# 2단계: 이동 중
elif stage == 1:
    start = html.escape(st.session_state.start)
    end = html.escape(st.session_state.end)

    st.markdown(f"""
    <div class="info">
        <p>오늘의 이동 경로</p>
        <div class="big">🚉 {start} → 🏁 {end}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status">
        <div style="font-size:60px">🚇</div>
        <div class="big">현재 이동 중이에요</div>
        <p>도착하면 아래 버튼을 눌러 주세요.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("실제 위치를 추적하지 않으므로 도착했을 때 직접 확인해 주세요.")

    if st.button("✅ 목적지에 도착했어요", type="primary"):
        st.session_state.arrived_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )
        st.session_state.stage = 2
        st.rerun()

    if st.button("← 이동 계획 다시 설정"):
        st.session_state.stage = 0
        st.rerun()

# 3단계: 도착 및 보호자 연락
else:
    end = html.escape(st.session_state.end)

    st.markdown(f"""
    <div class="status">
        <div style="font-size:65px">🎉</div>
        <div class="big">목적지에 도착했어요!</div>
        <p>{end} 도착 확인 완료</p>
    </div>
    """, unsafe_allow_html=True)

    st.success("보호자에게 도착 소식을 전해 주세요!")

    guardian = st.session_state.guardian
    phone = st.session_state.phone.replace("-", "").replace(" ", "")

    message = (
        f"안녕하세요, {guardian}님! "
        f"{st.session_state.start}에서 출발해 "
        f"{st.session_state.end}에 안전하게 도착했습니다. "
        f"도착 확인: {st.session_state.arrived_at}"
    )

    st.text_area("보호자에게 보낼 문자", value=message, height=120)

    sms_url = f"sms:{phone}?body={quote(message)}"

    st.markdown(
        f'<a class="sms" href="{html.escape(sms_url, quote=True)}">'
        '💌 보호자에게 문자 보내기</a>',
        unsafe_allow_html=True
    )

    st.caption(
        "휴대전화에서 문자 앱이 열립니다. "
        "실제 문자 전송은 직접 눌러야 합니다."
    )

    if st.button("🏠 처음으로 돌아가기", type="primary"):
        st.session_state.stage = 0
        st.rerun()

# 화면 안내
st.divider()
st.subheader("🔊 이용 안내")

if stage == 0:
    guide = "출발역, 도착역, 보호자 정보를 입력하고 이동 시작하기를 눌러 주세요."
elif stage == 1:
    guide = "목적지에 도착하면 도착 확인 버튼을 눌러 주세요."
else:
    guide = "보호자에게 문자 보내기 버튼을 눌러 연락해 주세요."

st.info(guide)
st.caption("휴대전화의 화면 읽기 기능으로 안내 문구를 들을 수 있습니다.")
