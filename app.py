
import streamlit as st
import html

st.set_page_config(
    page_title="SeniorCare 쉬운 키오스크",
    page_icon="🌸",
    layout="centered"
)

# 쉬운 말 사전
EASY_WORDS = {
    "테이크아웃": "포장해서 가져가기",
    "옵션 선택": "원하는 종류 고르기",
    "결제": "돈 내기",
    "카트": "담은 음식",
    "메뉴": "음식",
    "오더 완료": "주문이 끝났습니다",
}

# 상태 초기화
defaults = {
    "easy_mode": True,
    "font_size": "크게",
    "step": 1,
    "cart": {},
    "order_type": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def easy_text(text):
    if st.session_state.easy_mode:
        for old, new in EASY_WORDS.items():
            text = text.replace(old, new)
    return text

def go_to(step):
    st.session_state.step = step
    st.rerun()

# 음식 데이터
FOODS = [
    ("🍜", "잔치국수", 6000),
    ("🍚", "비빔밥", 8000),
    ("🍲", "된장찌개", 8000),
    ("🥟", "만두", 5000),
    ("🍛", "돈가스", 9000),
    ("🍵", "보리차", 2000)
]

PRICES = {name: price for _, name, price in FOODS}

# 글씨 크기
FONT_SIZES = {
    "보통": 18,
    "크게": 23,
    "아주 크게": 28
}

size = FONT_SIZES[st.session_state.font_size]

# 디자인
st.markdown(f"""
<style>
.stApp {{
    background: #FFF1F6;
    color: #333333;
}}

.block-container {{
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}}

h1 {{
    color: #C64C7D !important;
    font-size: {size + 18}px !important;
    font-weight: 800 !important;
}}

h2, h3 {{
    color: #A93F6C !important;
    font-size: {size + 5}px !important;
}}

.stMarkdown p {{
    font-size: {size}px;
    line-height: 1.6;
}}

div.stButton > button {{
    width: 100%;
    min-height: 85px;
    height: auto;
    padding: 12px 8px;
    border-radius: 20px;
    border: 2px solid #F4B3CD;
    background: white;
    color: #9D315D;
    box-shadow: 0 4px 12px rgba(200, 80, 120, 0.08);
}}

div.stButton > button p {{
    font-size: {size}px !important;
    font-weight: 700;
    white-space: normal;
    overflow-wrap: anywhere;
}}

div.stButton > button:hover {{
    background: #FFE0EC;
    border-color: #D84C84;
    color: #8C2452;
}}

div.stButton > button:focus-visible {{
    outline: 4px solid #245BC4;
    outline-offset: 2px;
}}

div.stButton > button:disabled {{
    opacity: 0.55;
}}

.food-card {{
    background: white;
    border-radius: 20px;
    padding: 18px 8px;
    text-align: center;
    border: 1px solid #F5D4E0;
    min-height: 155px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}}

.food-icon {{
    font-size: 48px;
}}

.food-name {{
    font-size: {size}px;
    font-weight: 800;
    color: #333333;
    overflow-wrap: anywhere;
}}

.food-price {{
    font-size: {max(size - 2, 16)}px;
    color: #C64C7D;
    font-weight: 700;
}}

.info-box {{
    background: #FFE0EC;
    border-radius: 18px;
    padding: 20px;
    font-size: {size}px;
    font-weight: 600;
    color: #7D2851;
    margin: 15px 0;
}}

.hero {{
    background: linear-gradient(135deg, #FFE1ED, #F9C4DA);
    border-radius: 26px;
    padding: 25px;
    margin-bottom: 20px;
    color: #8C2452;
}}

.hero-title {{
    font-size: {size + 10}px;
    font-weight: 800;
}}

.hero-sub {{
    font-size: {size}px;
}}

[data-testid="stMetricValue"] {{
    color: #C64C7D;
}}
</style>
""", unsafe_allow_html=True)

def info(text):
    safe = html.escape(str(text))
    st.markdown(
        f'<div class="info-box">{safe}</div>',
        unsafe_allow_html=True
    )

def add_item(name):
    cart = st.session_state.cart
    cart[name] = cart.get(name, 0) + 1
    st.rerun()

# 상단
st.markdown("""
<div class="hero">
    <div class="hero-title">🌸 SeniorCare</div>
    <div class="hero-sub">
        누구나 편하게 이용하는 쉬운 주문 키오스크
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("⚙️ 화면 설정", expanded=False):
    st.toggle(
        "어르신 모드 (쉬운 말 사용)",
        key="easy_mode"
    )

    st.radio(
        "글씨 크기",
        ["보통", "크게", "아주 크게"],
        key="font_size",
        horizontal=True
    )

st.divider()

# 1단계
if st.session_state.step == 1:
    st.header("① 이용 방법 선택")
    info("음식을 어디에서 드실 건가요?")

    if st.button("🍽️ 가게에서 먹기"):
        st.session_state.order_type = "매장"
        go_to(2)

    if st.button("🛍️ " + easy_text("테이크아웃")):
        st.session_state.order_type = "포장"
        go_to(2)

# 2단계
elif st.session_state.step == 2:
    st.header("② " + easy_text("메뉴") + " 고르기")
    info("원하는 음식을 눌러 주세요.")

    # 핵심: 2열 카드형 메뉴
    for i in range(0, len(FOODS), 2):
        cols = st.columns(2, gap="small")

        for j, col in enumerate(cols):
            index = i + j

            if index >= len(FOODS):
                continue

            emoji, name, price = FOODS[index]

            with col:
                st.markdown(
                    f"""
                    <div class="food-card">
                        <div class="food-icon">{emoji}</div>
                        <div class="food-name">{html.escape(name)}</div>
                        <div class="food-price">{price:,}원</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "➕ 담기",
                    key=f"add_{index}",
                    use_container_width=True
                ):
                    add_item(name)

        st.write("")

    st.divider()

    count = sum(st.session_state.cart.values())

    info(f"🛒 담은 음식: {count}개")

    if st.button(
        "💗 " + easy_text("카트") + " 확인하기",
        disabled=(count == 0)
    ):
        go_to(3)

    if st.button("⬅️ 이전으로"):
        go_to(1)

# 3단계
elif st.session_state.step == 3:
    st.header("③ 주문 확인")

    cart = st.session_state.cart

    if not cart:
        info("담은 음식이 없습니다.")
        if st.button("음식 고르러 가기"):
            go_to(2)
    else:
        total = 0

        for name, quantity in list(cart.items()):
            subtotal = PRICES[name] * quantity
            total += subtotal

            st.subheader(name)
            st.write(f"{quantity}개 / {subtotal:,}원")

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "➖ 빼기",
                    key=f"minus_{name}"
                ):
                    cart[name] -= 1
                    if cart[name] <= 0:
                        del cart[name]
                    st.rerun()

            with col2:
                if st.button(
                    "➕ 추가",
                    key=f"plus_{name}"
                ):
                    cart[name] += 1
                    st.rerun()

            st.divider()

        info(f"💰 모두 합쳐 {total:,}원입니다.")

        if st.button("💳 " + easy_text("결제") + "하기"):
            go_to(4)

        if st.button("⬅️ 음식 더 고르기"):
            go_to(2)

# 4단계
elif st.session_state.step == 4:
    st.header("④ 주문 완료")

    st.success("🎉 " + easy_text("오더 완료"))

    total = sum(
        PRICES[name] * quantity
        for name, quantity in st.session_state.cart.items()
    )

    info(f"주문 금액: {total:,}원")

    st.write("이용해 주셔서 감사합니다! 💗")
    st.info("연습용 화면으로 실제 돈은 나가지 않습니다.")

    if st.button("🔄 처음부터 다시 하기"):
        st.session_state.cart = {}
        st.session_state.order_type = ""
        go_to(1)

st.divider()
st.caption("SeniorCare | 어르신을 위한 쉬운 키오스크")
