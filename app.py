
import streamlit as st
from urllib.parse import quote

st.set_page_config(
    page_title="Korea Mate",
    page_icon="🌏",
    layout="centered"
)

# -------------------------------
# 디자인
# -------------------------------
st.markdown("""
<style>
.stApp {
    background: #FFFFFF;
    color: #111111;
}

.block-container {
    max-width: 1000px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.poster {
    position: relative;
    background: white;
    padding: 15px 0 35px;
    overflow: hidden;
}

.poster-title {
    font-family: Arial, sans-serif;
    font-size: clamp(70px, 15vw, 155px);
    font-weight: 900;
    letter-spacing: -0.095em;
    line-height: 0.85;
    color: #080808;
    margin: 0;
}

.poster-title span {
    display: block;
}

.poster-icons {
    display: flex;
    justify-content: space-between;
    font-size: 35px;
    margin: -5px 15px 5px;
    position: relative;
    z-index: 2;
}

.poster-sub {
    margin-top: 30px;
    font-size: 13px;
    letter-spacing: 3px;
    font-weight: bold;
    border-top: 2px solid black;
    padding-top: 15px;
}

.welcome {
    padding: 25px 0;
    border-top: 1px solid #111;
    border-bottom: 1px solid #111;
    margin-bottom: 25px;
}

.welcome h2 {
    font-size: 32px;
    color: #111;
    margin: 0;
}

.welcome p {
    font-size: 16px;
    color: #555;
}

div.stButton > button {
    background: white;
    border: 2px solid black;
    border-radius: 0;
    width: 100%;
    min-height: 115px;
    color: black;
    font-size: 20px;
    font-weight: 800;
    white-space: pre-line;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #111111;
    color: white;
    border-color: #111111;
}

div.stLinkButton > a {
    border-radius: 0;
}

h1, h2, h3 {
    color: #111111;
}

.stTextInput input,
.stTextArea textarea {
    border-radius: 0;
}

.small-label {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #666;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------
# AI 번역
# -------------------------------
def translate_text(text, language):
    try:
        from google import genai

        key = st.secrets.get("GEMINI_API_KEY", "")

        if not key:
            return "⚠️ Gemini API key is missing."

        client = genai.Client(api_key=key)

        prompt = f"""
        You are a friendly Korean travel guide.

        Explain the following Korean expression:
        {text}

        Target language: {language}

        Include:
        1. Natural translation
        2. Real meaning and nuance
        3. Cultural explanation
        4. Example sentence

        Respond in {language}.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        return response.text or "No result."

    except Exception:
        return "⚠️ Translation is unavailable. Please try again."


# -------------------------------
# 메뉴 상태
# -------------------------------
if "menu" not in st.session_state:
    st.session_state.menu = "home"


def go(menu):
    st.session_state.menu = menu
    st.rerun()


# -------------------------------
# 메인 화면
# -------------------------------
if st.session_state.menu == "home":

    st.markdown("""
    <div class="poster">
        <div class="poster-title">
            <span>Korea</span>
        </div>

        <div class="poster-icons">
            <span>🍜</span>
            <span>🇰🇷</span>
            <span>🏯</span>
        </div>

        <div class="poster-title">
            <span>Mate.</span>
        </div>

        <div class="poster-icons">
            <span>🚇</span>
            <span>🗺️</span>
            <span>🥢</span>
        </div>

        <div class="poster-sub">
            YOUR EASY GUIDE TO KOREA
            <span style="float:right">EST. 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome">
        <div class="small-label">01 / WELCOME</div>
        <h2>Welcome to Korea! 🇰🇷</h2>
        <p>
        한국 여행에 필요한 정보를 한곳에서!<br>
        Everything you need for your trip to Korea.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### EXPLORE KOREA ↗")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔤\nTRANSLATE\n번역기"):
            go("translate")

    with col2:
        if st.button("🗺️\nDIRECTIONS\n길안내"):
            go("directions")

    col3, col4 = st.columns(2)

    with col3:
        if st.button("🏪\nFIND PLACES\n시설 찾기"):
            go("places")

    with col4:
        if st.button("🎎\nCULTURE\n한국 문화"):
            go("culture")

    st.divider()

    st.markdown("### DID YOU KNOW? 💡")
    st.write(
        "**물은 셀프** means you should "
        "get your own water at a restaurant."
    )


# -------------------------------
# 번역기
# -------------------------------
elif st.session_state.menu == "translate":

    st.title("TRANSLATE 🔤")
    st.caption("KOREAN LANGUAGE GUIDE")

    language = st.selectbox(
        "Choose your language",
        [
            "English",
            "Chinese",
            "Japanese",
            "Vietnamese",
            "Thai",
            "Russian",
            "Spanish",
            "French"
        ]
    )

    text = st.text_area(
        "Korean expression",
        placeholder="밥 한번 먹자 / 갑분싸 / 물은 셀프"
    )

    if st.button("TRANSLATE ↗"):
        if not text.strip():
            st.warning("Please enter an expression.")
        elif len(text) > 500:
            st.warning("Maximum 500 characters.")
        else:
            with st.spinner("Translating..."):
                result = translate_text(text, language)
            st.info(result)

    st.subheader("POPULAR EXPRESSIONS")

    examples = {
        "밥 한번 먹자": "Let's eat sometime. Often a friendly expression.",
        "갑분싸": "The mood suddenly became awkward.",
        "물은 셀프": "Get your own water.",
        "아아": "Iced Americano.",
        "눈치": "Understanding social situations."
    }

    for word, meaning in examples.items():
        with st.expander(word):
            st.write(meaning)


# -------------------------------
# 길안내
# -------------------------------
elif st.session_state.menu == "directions":

    st.title("DIRECTIONS 🗺️")
    st.caption("EXPLORE KOREA")

    start = st.text_input(
        "Starting point",
        placeholder="Seoul Station"
    )

    destination = st.text_input(
        "Destination",
        placeholder="Gyeongbokgung"
    )

    if st.button("FIND ROUTE ↗"):
        if not start.strip() or not destination.strip():
            st.warning("Enter both locations.")
        else:
            keyword = quote(
                destination + " " + start + " 길찾기"
            )

            url = (
                "https://map.naver.com/p/search/"
                + keyword
            )

            st.link_button(
                "OPEN NAVER MAP ↗",
                url
            )

            st.caption(
                "Confirm your route on the map."
            )


# -------------------------------
# 시설 찾기
# -------------------------------
elif st.session_state.menu == "places":

    st.title("FIND PLACES 🏪")
    st.caption("YOUR TRAVEL ESSENTIALS")

    location = st.text_input(
        "Your area",
        placeholder="Hongdae, Seoul"
    )

    facilities = {
        "Convenience Store": "편의점",
        "Pharmacy": "약국",
        "Hospital": "병원",
        "Public Restroom": "공중화장실",
        "Subway Station": "지하철역",
        "Restaurant": "식당",
        "Tourist Information": "관광안내소"
    }

    selected = st.selectbox(
        "Select a facility",
        list(facilities.keys())
    )

    if st.button("SEARCH ↗"):
        if not location.strip():
            st.warning("Enter your area.")
        else:
            keyword = quote(
                location + " " + facilities[selected]
            )

            url = (
                "https://map.naver.com/p/search/"
                + keyword
            )

            st.link_button(
                "OPEN NAVER MAP ↗",
                url
            )


# -------------------------------
# 한국 문화
# -------------------------------
elif st.session_state.menu == "culture":

    st.title("KOREAN CULTURE 🎎")
    st.caption("LITTLE THINGS YOU SHOULD KNOW")

    tips = {
        "01 / WATER IS SELF-SERVICE 💧":
            "In many Korean restaurants, you get your own water.",

        "02 / SPOONS & CHOPSTICKS 🥢":
            "They may be inside a drawer under the table.",

        "03 / LET'S EAT SOMETIME 🍚":
            "'밥 한번 먹자' can be a friendly greeting, not a fixed plan.",

        "04 / TRANSPORTATION 🚇":
            "Use a transportation card and check tap-out rules.",

        "05 / SHOES OFF 👟":
            "Remove shoes in Korean homes and some restaurants.",

        "06 / RECYCLING ♻️":
            "Separate general waste, recyclables and food waste."
    }

    for title, description in tips.items():
        with st.expander(title):
            st.write(description)


# -------------------------------
# 돌아가기
# -------------------------------
if st.session_state.menu != "home":
    st.divider()

    if st.button("← BACK TO HOME"):
        go("home")


st.divider()
st.caption("KOREA MATE © 2026 | YOUR EASY GUIDE TO KOREA")
