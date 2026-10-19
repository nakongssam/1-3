
import streamlit as st
import html

# ---------------------------------
# 1. 기본 설정
# ---------------------------------
st.set_page_config(
    page_title="어르신 쉬운 키오스크",
    page_icon="👵",
    layout="centered"
)

# ---------------------------------
# 2. 어려운 말 -> 쉬운 말 사전
# ---------------------------------
EASY_WORDS = {
    "테이크아웃": "포장해서 가져가기",
    "딜리버리": "집으로 배달받기",
    "옵션 선택": "원하는 종류 고르기",
    "결제": "돈 내기",
    "카트": "담은 음식",
    "오더 완료": "주문이 끝났습니다",
    "메뉴": "음식",
    "수량": "개수",
    "취소": "그만두기",
    "컨펌": "확인하기",
    "키오스크": "무인 주문 기계",
    "영수증": "돈 낸 내역서"
}

def easy_text(text):
    text = str(text)
    if st.session_state.easy_mode:
        for old, new in sorted(
            EASY_WORDS.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):
            text = text.replace(old, new)
    return text

# ---------------------------------
# 3. 상태 저장
# ---------------------------------
if "easy_mode" not in st.session_state:
    st.session_state.easy_mode = True

if "font_size" not in st.session_state:
    st.session_state.font_size = "크게"

if "step" not in st.session_state:
    st.session_state.step = 1

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "order_type" not in st.session_state:
    st.session_state.order_type = ""

# ---------------------------------
# 4. 글씨 크기 및 디자인
# ---------------------------------
FONT_SIZES = {
    "보통": 20,
    "크게": 26,
    "아주 크게": 34
}

size = FONT_SIZES[st.session_state.font_size]

st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: sans-serif;
}}

.stApp {{
    background-color: #FFFDF5;
}}

h1 {{
    font-size: {size + 14}px !important;
    line-height: 1.4 !important;
}}

h2, h3 {{
    font-size: {size + 5}px !important;
    line-height: 1.5 !important;
}}

p, label, .stMarkdown,
[data-testid="stWidgetLabel"] {{
    font-size: {size}px !important;
    line-height: 1.6 !important;
}}

div.stButton > button {{
    min-height: 85px;
    height: auto;
    padding: 12px;
    border: 2px solid #333333;
    border-radius: 14px;
    background-color: #FFFFFF;
    color: #111111;
    width: 100%;
}}

div.stButton > button p {{
    font-size: {size}px !important;
    font-weight: bold;
    white-space: normal;
    overflow-wrap: anywhere;
}}

div.stButton > button:hover {{
    background-color: #FFF0B3;
    border-color: #333333;
    color: #111111;
}}

div.stButton > button:focus-visible {{
    outline: 4px solid #1668D8;
    outline-offset: 2px;
}}

.big-info {{
    font-size: {size}px;
    background-color: #FFF1B8;
    color: #111111;
    padding: 20px;
    border-radius: 12px;
    line-height: 1.6;
    margin: 12px 0;
    overflow-wrap: anywhere;
}}

.price {{
    font-size: {size}px;
    font-weight: bold;
    color: #111111;
}}

</style>
""", unsafe_allow_html=True)

def info(message):
    safe = html.escape(str(message))
    st.markdown(
        f'<div class="big-info">{safe}</div>',
        unsafe_allow_html=True
    )

def go_to(step):
    st.session_state.step = step
    st.rerun()

def add_item(name):
    cart = st.session_state.cart
    cart[name] = cart.get(name, 0) + 1
    st.rerun()

# ---------------------------------
# 5. 상단 설정
# ---------------------------------
st.title("👵 쉬운 주문 키오스크")
st.write("누구나 쉽고 편하게 주문할 수 있어요.")

with st.expander("⚙️ 화면 설정", expanded=True):
    st.toggle(
        "어르신 모드 (쉬운 말 사용)",
        key="easy_mode"
    )

    st.radio(
        "글씨 크기를 선택하세요",
        ["보통", "크게", "아주 크게"],
        horizontal=True,
        key="font_size"
    )

st.divider()

# ---------------------------------
# 6. 음식 데이터
# ---------------------------------
FOODS = {
    "🍜 잔치국수": 6000,
    "🍚 비빔밥": 8000,
    "🍲 된장찌개": 8000,
    "🥟 만두": 5000,
    "🍛 돈가스": 9000,
    "🍵 보리차": 2000
}

# ---------------------------------
# 7. 1단계: 이용 방법 선택
# ---------------------------------
if st.session_state.step == 1:
    st.header("1단계: 이용 방법 고르기")

    info("음식을 어디에서 드실 건가요?")

    if st.button("🍽️ 가게에서 먹기"):
        st.session_state.order_type = "가게에서 먹기"
        go_to(2)

    if st.button(
        "🛍️ " + easy_text("테이크아웃")
    ):
        st.session_state.order_type = "포장"
        go_to(2)

# ---------------------------------
# 8. 2단계: 음식 선택
# ---------------------------------
elif st.session_state.step == 2:
    st.header("2단계: " + easy_text("메뉴") + " 고르기")

    info("먹고 싶은 음식을 눌러 주세요.")

    for name, price in FOODS.items():
        st.markdown(
            f'<div class="price">{price:,}원</div>',
            unsafe_allow_html=True
        )

        if st.button(
            f"{name} 담기",
            key=f"add_{name}"
        ):
            add_item(name)

    st.divider()

    count = sum(st.session_state.cart.values())
    st.write(f"🛒 담은 음식: {count}개")

    if count > 0:
        if st.button("➡️ " + easy_text("카트") + " 확인"):
            go_to(3)
    else:
        info("음식을 하나 이상 골라 주세요.")

    if st.button("⬅️ 이전으로"):
        go_to(1)

# ---------------------------------
# 9. 3단계: 주문 확인
# ---------------------------------
elif st.session_state.step == 3:
    st.header("3단계: 주문 확인")

    cart = st.session_state.cart

    if not cart:
        info("담은 음식이 없습니다.")
        if st.button("음식 고르러 가기"):
            go_to(2)
    else:
        total = 0

        for name, quantity in list(cart.items()):
            price = FOODS.get(name, 0)
            subtotal = price * quantity
            total += subtotal

            st.subheader(name)
            st.write(
                f"{quantity}개 / {subtotal:,}원"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "➖ 한 개 빼기",
                    key=f"minus_{name}"
                ):
                    cart[name] -= 1
                    if cart[name] <= 0:
                        del cart[name]
                    st.rerun()

            with col2:
                if st.button(
                    "➕ 한 개 추가",
                    key=f"plus_{name}"
                ):
                    cart[name] += 1
                    st.rerun()

            st.divider()

        info(f"모두 합쳐 {total:,}원입니다.")

        if st.button("💳 " + easy_text("결제") + "하기"):
            go_to(4)

        if st.button("⬅️ 음식 더 고르기"):
            go_to(2)

# ---------------------------------
# 10. 4단계: 주문 완료
# ---------------------------------
elif st.session_state.step == 4:
    st.header("4단계: 주문 완료")

    st.success("🎉 " + easy_text("오더 완료"))

    total = sum(
        FOODS.get(name, 0) * quantity
        for name, quantity
        in st.session_state.cart.items()
    )

    info(
        f"주문 금액은 {total:,}원입니다. "
        "이 화면은 연습용입니다. "
        "실제로 돈이 나가지 않습니다."
    )

    st.write("이용해 주셔서 감사합니다. 😊")

    if st.button("🔄 처음부터 다시 하기"):
        st.session_state.cart = {}
        st.session_state.order_type = ""
        go_to(1)

# ---------------------------------
# 11. 하단 안내
# ---------------------------------
st.divider()
st.caption(
    "본 앱은 어르신을 위한 키오스크 연습용입니다. "
    "실제 주문이나 결제는 진행되지 않습니다."
)
