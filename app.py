

import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(
    page_title="서비스 사용 설명",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 상태 저장
if "page" not in st.session_state:
    st.session_state.page = "main"

if "speed" not in st.session_state:
    st.session_state.speed = 1.0

if "speech" not in st.session_state:
    st.session_state.speech = ""

if "speech_id" not in st.session_state:
    st.session_state.speech_id = 0


def speak(message):
    st.session_state.speech = message
    st.session_state.speech_id += 1


def change_page(page):
    st.session_state.page = page


# 음성 출력: 브라우저의 한국어 음성 기능 사용
def voice_player():
    message = json.dumps(
        st.session_state.speech,
        ensure_ascii=False
    )
    speed = st.session_state.speed
    speech_id = st.session_state.speech_id

    components.html(
        f"""
        <script>
        const message = {message};
        const speed = {speed};
        const speechId = {speech_id};
        const synth = window.parent.speechSynthesis;

        try {{
            if (window.parent._lastSpeechId !== speechId) {{
                window.parent._lastSpeechId = speechId;
                synth.cancel();

                if (message) {{
                    const utterance =
                        new SpeechSynthesisUtterance(message);
                    utterance.lang = "ko-KR";
                    utterance.rate = speed;
                    utterance.volume = 1;
                    synth.speak(utterance);
                }}
            }}
        }} catch (error) {{
            console.log("음성 안내 오류:", error);
        }}
        </script>
        """,
        height=0
    )


# 디자인
st.markdown("""
<style>
.stApp {
    background-color: #FFFFFF;
    color: #111111;
}

.block-container {
    max-width: 1100px;
    padding-top: 1rem;
}

h1, h2, h3, p {
    color: #111111 !important;
}

div.stButton > button {
    width: 100%;
    min-height: 105px;
    font-size: 25px !important;
    font-weight: bold !important;
    border: 3px solid #111111 !important;
    border-radius: 10px !important;
    white-space: pre-wrap;
}

div.stButton > button:focus-visible {
    outline: 5px solid #111111 !important;
    outline-offset: 3px;
}

/* 빠르게 */
div.st-key-fast1 button,
div.st-key-fast2 button {
    background-color: #FF1717 !important;
    color: #FFFFFF !important;
}

/* 느리게 */
div.st-key-slow1 button,
div.st-key-slow2 button {
    background-color: #1554C9 !important;
    color: #FFFFFF !important;
}

/* 기능 1 */
div.st-key-feature1 button {
    background-color: #00F000 !important;
    color: #000000 !important;
    min-height: 245px;
    font-size: 32px !important;
}

/* 기능 2 */
div.st-key-feature2 button {
    background-color: #FFFF00 !important;
    color: #000000 !important;
    min-height: 245px;
    font-size: 32px !important;
}

/* 기타 버튼 */
div.st-key-home button,
div.st-key-listen button,
div.st-key-bus_speak button {
    background-color: #FFDD33 !important;
    color: #000000 !important;
}

div[data-testid="stTextInput"] input {
    font-size: 26px;
    min-height: 65px;
    border: 3px solid black;
}
</style>
""", unsafe_allow_html=True)


# 제목
st.title("🚌 서비스 사용 설명")
st.write("시각장애인을 위한 쉬운 버스 음성 안내 서비스")

# 음성 속도 조절
st.subheader("🔊 음성 속도 조절")

c1, c2, c3, c4 = st.columns(4, gap="small")

with c1:
    if st.button("빠르게 ⏩", key="fast1"):
        st.session_state.speed = min(
            2.0, round(st.session_state.speed + 0.25, 2)
        )
        speak("음성 속도를 빠르게 설정했습니다.")

with c2:
    if st.button("느리게 🐢", key="slow1"):
        st.session_state.speed = max(
            0.5, round(st.session_state.speed - 0.25, 2)
        )
        speak("음성 속도를 느리게 설정했습니다.")

with c3:
    if st.button("빠르게 ⏩", key="fast2"):
        st.session_state.speed = min(
            2.0, round(st.session_state.speed + 0.25, 2)
        )
        speak("음성 속도를 빠르게 설정했습니다.")

with c4:
    if st.button("느리게 🐢", key="slow2"):
        st.session_state.speed = max(
            0.5, round(st.session_state.speed - 0.25, 2)
        )
        speak("음성 속도를 느리게 설정했습니다.")

st.write(f"현재 음성 속도: {st.session_state.speed}배")


# 메인 페이지
if st.session_state.page == "main":

    st.subheader("원하는 기능을 선택하세요")

    left, right = st.columns(2, gap="small")

    with left:
        if st.button(
            "🚌 기능 1\n버스 번호 안내",
            key="feature1"
        ):
            change_page("bus")
            speak(
                "버스 번호 안내 페이지입니다. "
                "버스 번호를 입력하고 안내 듣기 버튼을 누르세요."
            )
            st.rerun()

    with right:
        if st.button(
            "🔊 기능 2\n서비스 사용 설명",
            key="feature2"
        ):
            change_page("help")
            speak(
                "서비스 사용 설명 페이지입니다. "
                "음성 안내 듣기 버튼을 누르면 "
                "사용 방법을 들을 수 있습니다."
            )
            st.rerun()

    st.info(
        "💡 초록색은 버스 번호 안내, "
        "노란색은 서비스 사용 설명입니다."
    )


# 기능 1: 버스 번호 음성 안내
elif st.session_state.page == "bus":

    st.header("🟢 기능 1: 버스 번호 안내")

    st.write(
        "버스 번호를 입력하면 해당 번호를 "
        "큰 글씨와 음성으로 알려드립니다."
    )

    bus_number = st.text_input(
        "버스 번호를 입력하세요",
        placeholder="예: 100, 12, 700"
    )

    if st.button("🔊 버스 번호 음성 안내", key="bus_speak"):
        if bus_number.strip():
            number = bus_number.strip()

            st.success(f"🚌 {number}번 버스")

            speak(
                f"{number}번 버스입니다. "
                "탑승 전 버스 번호와 목적지를 "
                "다시 확인해 주세요."
            )
        else:
            st.warning("버스 번호를 입력해 주세요.")
            speak("버스 번호를 입력해 주세요.")

    st.warning(
        "이 기능은 입력된 번호를 읽어 주는 "
        "연습용 기능입니다. 실제 도착 버스를 "
        "자동으로 확인하지 않습니다."
    )

    if st.button("🏠 메인 페이지로 이동", key="home"):
        change_page("main")
        speak("메인 페이지로 이동했습니다.")
        st.rerun()


# 기능 2: 서비스 사용 설명
elif st.session_state.page == "help":

    st.header("🟡 기능 2: 서비스 사용 설명")

    explanation = (
        "안녕하세요. 시각장애인을 위한 "
        "버스 안내 서비스입니다. "
        "이 서비스는 버스 번호를 음성으로 "
        "알려 주는 연습용 앱입니다. "
        "첫 번째, 빨간색 빠르게 버튼을 누르면 "
        "음성 속도가 빨라집니다. "
        "두 번째, 파란색 느리게 버튼을 누르면 "
        "음성 속도가 느려집니다. "
        "세 번째, 초록색 기능 1 버튼을 누르면 "
        "버스 번호 안내 페이지로 이동합니다. "
        "네 번째, 노란색 기능 2 버튼을 누르면 "
        "서비스 사용 방법을 확인할 수 있습니다. "
        "화면 아래의 메인 페이지 버튼을 누르면 "
        "처음 화면으로 돌아갑니다."
    )

    st.write("### 📖 사용 방법")
    st.write("🔴 빨간색: 음성 빠르게")
    st.write("🔵 파란색: 음성 느리게")
    st.write("🟢 초록색: 버스 번호 안내")
    st.write("🟡 노란색: 서비스 사용 설명")

    if st.button("🔊 전체 사용 설명 듣기", key="listen"):
        speak(explanation)

    if st.button("🏠 메인 페이지로 이동", key="home"):
        change_page("main")
        speak("메인 페이지로 이동했습니다.")
        st.rerun()


# 음성 재생
voice_player()
