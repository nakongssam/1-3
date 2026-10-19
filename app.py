
import streamlit as st
import streamlit.components.v1 as components
import json

# ----------------------------------
# 기본 설정
# ----------------------------------
st.set_page_config(
    page_title="BUS MATE",
    page_icon="🚌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------------------------
# 상태 관리
# ----------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "speed" not in st.session_state:
    st.session_state.speed = 1.0

if "speech" not in st.session_state:
    st.session_state.speech = ""

if "speech_id" not in st.session_state:
    st.session_state.speech_id = 0


def speak(message):
    st.session_state.speech = message
    st.session_state.speech_id += 1


def move_page(page, message):
    st.session_state.page = page
    speak(message)


# ----------------------------------
# 음성 안내
# ----------------------------------
def play_voice():
    message = json.dumps(
        st.session_state.speech,
        ensure_ascii=False
    )

    speed = st.session_state.speed
    speech_id = st.session_state.speech_id

    components.html(
        f"""
        <script>
        try {{
            const synth = window.parent.speechSynthesis;
            const message = {message};
            const speechId = {speech_id};
            const speed = {speed};

            if (window.parent.busMateSpeechId !== speechId) {{
                window.parent.busMateSpeechId = speechId;
                synth.cancel();

                if (message) {{
                    const utterance =
                        new SpeechSynthesisUtterance(message);

                    utterance.lang = "ko-KR";
                    utterance.rate = speed;
                    utterance.pitch = 1;
                    utterance.volume = 1;

                    synth.speak(utterance);
                }}
            }}
        }} catch (error) {{
            console.log("음성 재생 오류:", error);
        }}
        </script>
        """,
        height=0
    )


# ----------------------------------
# 디자인 CSS
# ----------------------------------
st.markdown("""
<style>

/* 전체 배경 */
.stApp {
    background: #FBEAE6;
    color: #342F30;
}

/* 모바일 앱처럼 중앙 배치 */
.block-container {
    max-width: 540px;
    background: #FFFEFD;
    padding: 30px 25px 45px;
    border-radius: 32px;
    margin-top: 25px;
    margin-bottom: 25px;
    box-shadow: 0 12px 40px rgba(196, 126, 126, 0.12);
}

/* 제목 */
h1, h2, h3 {
    color: #393031 !important;
    font-family: sans-serif;
}

h1 {
    font-size: 35px !important;
    font-weight: 750 !important;
}

h2 {
    font-size: 26px !important;
}

p {
    color: #635A5B;
}

/* 버튼 기본 스타일 */
div.stButton > button {
    width: 100%;
    min-height: 68px;
    border-radius: 20px;
    border: 1px solid #E6CBC6;
    background: #F8E2DE;
    color: #463638;
    font-size: 19px;
    font-weight: 650;
    white-space: pre-wrap;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #F1CBC5;
    border-color: #DDA7A0;
    color: #33282A;
}

div.stButton > button:focus-visible {
    outline: 4px solid #7D4050;
    outline-offset: 3px;
}

/* 기능 카드 */
div.st-key-bus_card button {
    min-height: 190px;
    background: #F4D6D1;
    color: #493034;
    font-size: 24px;
    border: none;
}

div.st-key-help_card button {
    min-height: 190px;
    background: #FAE9DB;
    color: #493B31;
    font-size: 24px;
    border: none;
}

/* 음성 속도 버튼 */
div.st-key-slow button,
div.st-key-normal button,
div.st-key-fast button {
    min-height: 65px;
    font-size: 15px;
    padding: 5px;
}

div.st-key-normal button {
    background: #F3CFC9;
}

/* 하단 이동 버튼 */
div.st-key-nav_home button,
div.st-key-nav_bus button,
div.st-key-nav_help button {
    min-height: 70px;
    font-size: 14px;
    padding: 5px;
    background: #FFF2EE;
}

/* 입력창 */
div[data-testid="stTextInput"] input {
    background: #FFF8F6;
    border: 2px solid #DCAFA8;
    border-radius: 15px;
    min-height: 65px;
    font-size: 24px;
    color: #30282A;
}

/* 안내 박스 */
.soft-card {
    background: #FCECE8;
    padding: 22px;
    border-radius: 22px;
    margin: 18px 0;
}

.soft-card p {
    margin-bottom: 8px;
}

.soft-title {
    font-size: 22px;
    font-weight: 750;
    color: #463437;
}

.soft-desc {
    font-size: 15px;
    color: #766769;
    line-height: 1.8;
}

.small-label {
    font-size: 14px;
    font-weight: 650;
    letter-spacing: 1px;
    color: #B47D7D;
}

.hero {
    padding: 28px 0 16px;
}

.hero-title {
    font-size: 33px;
    font-weight: 750;
    line-height: 1.4;
    color: #342B2D;
}

.hero-sub {
    font-size: 16px;
    line-height: 1.8;
    color: #807274;
}

.section-title {
    font-size: 20px;
    font-weight: 750;
    margin: 25px 0 15px;
    color: #3E3335;
}

.bus-result {
    background: #F7DAD5;
    border-radius: 25px;
    text-align: center;
    padding: 30px 15px;
    margin: 20px 0;
    color: #34282B;
    font-size: 32px;
    font-weight: bold;
    overflow-wrap: anywhere;
}

.footer {
    text-align: center;
    color: #A98E8E;
    font-size: 12px;
    margin-top: 28px;
}

/* 작은 화면 */
@media (max-width: 600px) {
    .block-container {
        margin: 0;
        padding: 20px 15px 35px;
        border-radius: 0;
        box-shadow: none;
    }

    .hero-title {
        font-size: 28px;
    }

    div.stButton > button {
        font-size: 16px;
    }

    div.st-key-bus_card button,
    div.st-key-help_card button {
        font-size: 18px;
        min-height: 165px;
    }
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------
# 상단 로고
# ----------------------------------
st.markdown(
    '<div class="small-label">🚌 BUS MATE</div>',
    unsafe_allow_html=True
)


# ----------------------------------
# 음성 속도 조절 (모든 페이지 공통)
# ----------------------------------
def speed_control():

    st.markdown(
        '<div class="section-title">🔊 음성 속도 설정</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        if st.button("🐢 느리게", key="slow"):
            st.session_state.speed = 0.7
            speak("느린 속도로 안내합니다.")

    with c2:
        if st.button("🌷 보통", key="normal"):
            st.session_state.speed = 1.0
            speak("보통 속도로 안내합니다.")

    with c3:
        if st.button("⏩ 빠르게", key="fast"):
            st.session_state.speed = 1.4
            speak("빠른 속도로 안내합니다.")

    st.caption(
        f"현재 음성 속도: {st.session_state.speed}배"
    )


# ----------------------------------
# 홈 페이지
# ----------------------------------
if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">
            안녕하세요! 👋<br>
            오늘도 편안한 이동을<br>
            도와드릴게요.
        </div>
        <div class="hero-sub">
            버스 이용이 조금 더 쉬워지는 순간,<br>
            BUS MATE가 함께합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="soft-card">
        <div class="soft-title">
            🌸 당신의 이동을 응원해요
        </div>
        <div class="soft-desc">
            큰 버튼과 음성 안내로
            쉽고 편리하게 이용할 수 있어요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    speed_control()

    st.markdown(
        '<div class="section-title">어떤 도움이 필요하세요?</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2, gap="small")

    with left:
        if st.button(
            "🚌\n\n버스 번호\n안내",
            key="bus_card"
        ):
            move_page(
                "bus",
                "버스 번호 안내 페이지입니다. "
                "버스 번호를 입력해 주세요."
            )
            st.rerun()

    with right:
        if st.button(
            "📖\n\n서비스\n사용 설명",
            key="help_card"
        ):
            move_page(
                "help",
                "서비스 사용 설명 페이지입니다."
            )
            st.rerun()

    st.markdown("""
    <div class="soft-card">
        <div class="soft-title">
            💗 함께하는 안전한 이동
        </div>
        <div class="soft-desc">
            원하는 기능을 선택하면
            음성으로 사용 방법을 알려드려요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔊 첫 화면 음성 안내 듣기"):
        speak(
            "안녕하세요. 버스 메이트입니다. "
            "이 앱은 버스 번호를 음성으로 안내하는 "
            "연습용 서비스입니다. "
            "버스 번호 안내 또는 서비스 사용 설명 "
            "버튼을 선택해 주세요."
        )


# ----------------------------------
# 버스 번호 안내 페이지
# ----------------------------------
elif st.session_state.page == "bus":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">
            🚌 버스 번호 안내
        </div>
        <div class="hero-sub">
            버스 번호를 입력하면<br>
            음성으로 읽어드릴게요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="soft-card">
        <div class="soft-title">
            🌷 어떤 버스를 찾으세요?
        </div>
        <div class="soft-desc">
            아래 입력창에 버스 번호를 입력하세요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    bus_number = st.text_input(
        "버스 번호",
        placeholder="예: 100, 12, 700",
        max_chars=20
    )

    if st.button("🔊 버스 번호 음성으로 듣기"):

        number = bus_number.strip()

        if number:
            st.session_state.last_bus = number

            speak(
                f"{number}번 버스입니다. "
                "실제 도착 버스 번호는 "
                "별도로 확인해 주세요."
            )
        else:
            st.warning("버스 번호를 입력해 주세요.")
            speak("버스 번호를 입력해 주세요.")

    if "last_bus" in st.session_state:
        safe_number = (
            st.session_state.last_bus
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

        st.markdown(
            f'<div class="bus-result">🚌 {safe_number}번 버스</div>',
            unsafe_allow_html=True
        )

    st.info(
        "이 기능은 입력한 번호를 읽어 주는 "
        "시연용 기능입니다. 실제 도착 버스를 "
        "자동으로 인식하지는 않습니다."
    )

    speed_control()


# ----------------------------------
# 서비스 사용 설명 페이지
# ----------------------------------
elif st.session_state.page == "help":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">
            📖 서비스 사용 설명
        </div>
        <div class="hero-sub">
            BUS MATE 사용 방법을<br>
            차근차근 알려드릴게요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="soft-card">
        <div class="soft-title">
            01. 음성 속도 조절
        </div>
        <div class="soft-desc">
            느리게, 보통, 빠르게 버튼 중
            원하는 속도를 선택하세요.
        </div>
    </div>

    <div class="soft-card">
        <div class="soft-title">
            02. 버스 번호 안내
        </div>
        <div class="soft-desc">
            버스 번호를 입력한 뒤
            음성 안내 버튼을 누르세요.
        </div>
    </div>

    <div class="soft-card">
        <div class="soft-title">
            03. 페이지 이동
        </div>
        <div class="soft-desc">
            화면 아래쪽의 큰 버튼을 눌러
            원하는 페이지로 이동할 수 있어요.
        </div>
    </div>
    """, unsafe_allow_html=True)

    explanation = (
        "안녕하세요. 버스 메이트입니다. "
        "이 앱은 시각장애인을 위한 "
        "버스 번호 음성 안내 연습용 서비스입니다. "
        "첫 번째, 음성 속도를 조절할 수 있습니다. "
        "느리게, 보통, 빠르게 버튼을 선택하세요. "
        "두 번째, 버스 번호 안내 페이지에서는 "
        "번호를 입력하고 음성으로 들을 수 있습니다. "
        "세 번째, 화면 아래의 메뉴 버튼으로 "
        "다른 페이지로 이동할 수 있습니다. "
        "이 앱은 실제 도착 버스를 자동으로 "
        "인식하지 않습니다."
    )

    if st.button("🔊 전체 사용 설명 듣기"):
        speak(explanation)

    speed_control()


# ----------------------------------
# 하단 내비게이션
# ----------------------------------
st.markdown("---")

nav1, nav2, nav3 = st.columns(3, gap="small")

with nav1:
    if st.button("🏠\n홈", key="nav_home"):
        move_page(
            "home",
            "홈 화면으로 이동했습니다."
        )
        st.rerun()

with nav2:
    if st.button("🚌\n버스 안내", key="nav_bus"):
        move_page(
            "bus",
            "버스 번호 안내 페이지입니다."
        )
        st.rerun()

with nav3:
    if st.button("📖\n사용 설명", key="nav_help"):
        move_page(
            "help",
            "서비스 사용 설명 페이지입니다."
        )
        st.rerun()


# ----------------------------------
# 하단 문구
# ----------------------------------
st.markdown("""
<div class="footer">
    Made with 💗 BUS MATE<br>
    당신의 편안한 이동을 응원합니다.
</div>
""", unsafe_allow_html=True)


# ----------------------------------
# 음성 재생 실행
# ----------------------------------
play_voice()
