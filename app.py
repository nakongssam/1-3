

import streamlit as st
from urllib.parse import quote

# =====================================
# 1. 페이지 기본 설정
# =====================================
st.set_page_config(
    page_title="Korea Mate",
    page_icon="🌏",
    layout="centered"
)

# =====================================
# 2. 디자인 설정
# =====================================
st.markdown("""
<style>
.stApp {
    background-color: #FFF9FB;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

.main-title {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    color: #E85D85;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #555;
    margin-bottom: 25px;
}

.welcome-box {
    background-color: #FFE8F0;
    padding: 28px 15px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
}

.welcome-title {
    font-size: 26px;
    font-weight: bold;
    color: #333;
}

.welcome-text {
    font-size: 17px;
    color: #555;
    margin-top: 10px;
}

div.stButton > button {
    width: 100%;
    height: 125px;
    background-color: white;
    border: 2px solid #F5B6C9;
    border-radius: 16px;
    color: #333;
    font-size: 20px;
    font-weight: bold;
    white-space: pre-line;
}

div.stButton > button:hover {
    background-color: #FFE3ED;
    border-color: #E85D85;
    color: #D94C75;
}

h2, h3 {
    color: #D94C75;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# 3. AI 번역 함수
# =====================================
def translate_text(text, language):
    try:
        from google import genai

        api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            return "⚠️ Gemini API key is missing."

        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are Korea Mate, a friendly Korean travel guide.

        Explain this Korean expression to a foreign traveler.

        Expression: {text}
        Target language: {language}

        Include:
        1. Natural translation
        2. Real meaning and nuance
        3. Korean cultural context
        4. Example sentence

        Answer in {language}.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        if response.text:
            return response.text

        return "Translation result is empty."

    except Exception:
        return (
            "⚠️ Translation failed. "
            "Please check your API key and try again."
        )


# =====================================
# 4. 메뉴 상태 관리
# =====================================
if "menu" not in st.session_state:
    st.session_state.menu = "home"


def change_menu(menu):
    st.session_state.menu = menu


# =====================================
# 5. 상단 로고
# =====================================
st.markdown(
    '<div class="main-title">Korea Mate 🌏</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Your Easy Guide to Korea'
    '</div>',
    unsafe_allow_html=True
)


# =====================================
# 6. 메인 화면
# =====================================
if st.session_state.menu == "home":

    st.markdown("""
    <div class="welcome-box">
        <div class="welcome-title">
            🇰🇷 Welcome to Korea!
        </div>
        <div class="welcome-text">
            한국 여행에 필요한 정보를 한곳에서!<br>
            Everything you need for your trip to Korea!
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔤 번역기\nTranslation",
            use_container_width=True
        ):
            change_menu("translate")
            st.rerun()

    with col2:
        if st.button(
            "🗺️ 길안내\nDirections",
            use_container_width=True
        ):
            change_menu("directions")
            st.rerun()

    col3, col4 = st.columns(2)

    with col3:
        if st.button(
            "🏪 시설 찾기\nFind Places",
            use_container_width=True
        ):
            change_menu("places")
            st.rerun()

    with col4:
        if st.button(
            "🎎 한국 문화\nKorean Culture",
            use_container_width=True
        ):
            change_menu("culture")
            st.rerun()

    st.divider()

    st.info(
        "✨ Select a menu to start your Korea adventure!"
    )

    st.markdown("### 💡 Today's Korea Tip")

    st.write(
        "🍽️ **물은 셀프** means you should "
        "get your own water at a restaurant."
    )


# =====================================
# 7. 번역기 페이지
# =====================================
elif st.session_state.menu == "translate":

    st.header("🔤 Korean Translator")

    st.write(
        "Understand Korean slang, abbreviations "
        "and everyday expressions!"
    )

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
        "Enter a Korean expression",
        placeholder="예: 밥 한번 먹자, 갑분싸, 물은 셀프"
    )

    if st.button("✨ Translate & Explain"):
        if not text.strip():
            st.warning("Please enter a Korean expression.")
        elif len(text) > 500:
            st.warning("Please enter 500 characters or fewer.")
        else:
            with st.spinner("Translating..."):
                result = translate_text(text, language)

            st.markdown("### 📖 Explanation")
            st.info(result)

    st.subheader("💬 Popular Korean Expressions")

    examples = {
        "밥 한번 먹자": (
            "Let's eat sometime. "
            "It may be a friendly greeting, "
            "not an actual appointment."
        ),
        "갑분싸": (
            "The atmosphere suddenly became awkward."
        ),
        "물은 셀프": (
            "Please get your own water."
        ),
        "아아": (
            "Short for iced Americano."
        ),
        "눈치": (
            "The ability to understand "
            "social situations and others' feelings."
        )
    }

    for word, meaning in examples.items():
        with st.expander(word):
            st.write(meaning)


# =====================================
# 8. 길안내 페이지
# =====================================
elif st.session_state.menu == "directions":

    st.header("🗺️ Directions")

    st.write("Find your way around Korea!")

    start = st.text_input(
        "Starting Point",
        placeholder="Seoul Station"
    )

    destination = st.text_input(
        "Destination",
        placeholder="Gyeongbokgung Palace"
    )

    if st.button("🔎 Search Directions"):

        if not start.strip() or not destination.strip():
            st.warning("Please enter both locations.")
        else:
            keyword = quote(
                destination + " " + start + " 길찾기"
            )

            url = (
                "https://map.naver.com/p/search/"
                + keyword
            )

            st.success("Your map is ready!")

            st.link_button(
                "🗺️ Open Naver Map",
                url
            )

            st.caption(
                "Confirm your route in Naver Map."
            )


# =====================================
# 9. 시설 찾기 페이지
# =====================================
elif st.session_state.menu == "places":

    st.header("🏪 Find Places")

    st.write(
        "Find useful facilities during your trip."
    )

    location = st.text_input(
        "Enter your location",
        placeholder="Hongdae, Seoul"
    )

    place_type = st.selectbox(
        "Choose a facility",
        [
            "Convenience Store",
            "Pharmacy",
            "Hospital",
            "Public Restroom",
            "Subway Station",
            "Restaurant",
            "Tourist Information Center"
        ]
    )

    place_names = {
        "Convenience Store": "편의점",
        "Pharmacy": "약국",
        "Hospital": "병원",
        "Public Restroom": "공중화장실",
        "Subway Station": "지하철역",
        "Restaurant": "식당",
        "Tourist Information Center": "관광안내소"
    }

    if st.button("🔎 Search Places"):

        if not location.strip():
            st.warning("Please enter your location.")
        else:
            keyword = quote(
                location + " " + place_names[place_type]
            )

            url = (
                "https://map.naver.com/p/search/"
                + keyword
            )

            st.link_button(
                "📍 Open Naver Map",
                url
            )


# =====================================
# 10. 한국 문화 페이지
# =====================================
elif st.session_state.menu == "culture":

    st.header("🎎 Korean Culture Guide")

    st.write(
        "Learn useful Korean customs "
        "before and during your trip!"
    )

    culture_data = {
        "🍽️ Water is Self-Service": (
            "In many Korean restaurants, "
            "customers get their own water."
        ),

        "🥄 Spoon and Chopsticks": (
            "Spoons and chopsticks may be "
            "in a drawer under the table."
        ),

        "🍚 Let's Eat Sometime": (
            "'밥 한번 먹자' is often a friendly "
            "expression rather than a fixed plan."
        ),

        "🚌 Public Transportation": (
            "Use a transportation card and "
            "check whether you need to tap "
            "when getting off."
        ),

        "👟 Shoes Off": (
            "Remove your shoes when entering "
            "Korean homes and some traditional places."
        ),

        "♻️ Recycling": (
            "Korea separates general waste, "
            "recyclables and food waste."
        )
    }

    for title, description in culture_data.items():
        with st.expander(title):
            st.write(description)


# =====================================
# 11. 홈으로 돌아가기
# =====================================
if st.session_state.menu != "home":

    st.divider()

    if st.button("🏠 Back to Home"):
        change_menu("home")
        st.rerun()


# =====================================
# 12. 하단
# =====================================
st.divider()

st.caption(
    "🌏 Korea Mate | Your Easy Guide to Korea"
)
