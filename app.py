"""
듀오RINGGO - 이주시민을 위한 한국어·한국문화 학습 앱
공감 대상: 이주시민
문제: 언어 및 문화 차이로 인해 오해와 갈등이 생김
"""

import html
import io
import json
import random
import re

import streamlit as st

# ---------------------------------------------------------
# 선택 라이브러리 (없어도 앱이 멈추지 않도록 처리)
# ---------------------------------------------------------
try:
    from gtts import gTTS
    GTTS_OK = True
except Exception:
    GTTS_OK = False

try:
    from google import genai
    from google.genai import types
    GENAI_OK = True
except Exception:
    GENAI_OK = False

MODEL = "gemini-2.5-flash-lite"

st.set_page_config(page_title="듀오RINGGO", page_icon="🔔", layout="wide")

# ---------------------------------------------------------
# 디자인 (파스텔 블루 · 둥근 카드 · 큰 글씨)
# ---------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.stApp {
    font-family: 'Noto Sans KR', sans-serif;
    background: linear-gradient(180deg, #e3eeff 0%, #f4f8ff 45%, #e9f2ff 100%);
    color: #1e2a4a;
    word-break: keep-all;
}
.stApp input, .stApp button, .stApp textarea { font-family: 'Noto Sans KR', sans-serif; }
.block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1350px; }
header[data-testid="stHeader"] { background: transparent; }

/* 기본 글자 크게 */
.stApp p, .stApp li, .stApp label { font-size: 1.15rem; line-height: 1.7; color: #1e2a4a; }

/* ---------- 상단 배너 ---------- */
.hero {
    position: relative; overflow: hidden;
    background: linear-gradient(135deg, #6fa8ff 0%, #8fc3ff 45%, #cfe6ff 100%);
    border-radius: 32px; padding: 1.6rem 2rem 1.8rem; margin-bottom: 1.5rem;
    box-shadow: 0 14px 40px rgba(80, 130, 230, 0.25); color: #ffffff;
}
.hero::after {
    content: ""; position: absolute; right: -80px; top: -80px; width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0) 70%);
}
.hero-top { display: flex; align-items: center; gap: 0.8rem; position: relative; z-index: 1; }
.avatar {
    width: 52px; height: 52px; border-radius: 50%; background: rgba(255,255,255,0.35);
    display: flex; align-items: center; justify-content: center; font-size: 1.7rem;
}
.hello { font-size: 1.3rem; font-weight: 700; line-height: 1.3; }
.hello small { font-size: 0.95rem; font-weight: 400; opacity: 0.9; }
.bell {
    margin-left: auto; width: 52px; height: 52px; border-radius: 16px;
    background: rgba(255,255,255,0.35); display: flex; align-items: center;
    justify-content: center; font-size: 1.6rem;
}
.hero-title {
    position: relative; z-index: 1; font-size: 3.4rem; font-weight: 900;
    letter-spacing: -1px; margin-top: 1rem; line-height: 1.1;
    text-shadow: 0 4px 18px rgba(40, 90, 200, 0.25);
}
.hero-sub { position: relative; z-index: 1; font-size: 1.3rem; margin-top: 0.4rem; opacity: 0.95; }
.chips { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: 0.6rem; margin-top: 1.1rem; }
.chips span {
    background: rgba(255,255,255,0.9); color: #3b6fd8; font-weight: 700;
    padding: 0.45rem 1.1rem; border-radius: 999px; font-size: 1.05rem;
    box-shadow: 0 4px 12px rgba(60, 110, 220, 0.15);
}

/* ---------- 흰색 카드 ---------- */
[class*="st-key-card"] {
    background: #ffffff; border-radius: 28px; padding: 1.5rem 1.5rem 1.6rem;
    box-shadow: 0 10px 32px rgba(80, 120, 220, 0.13);
}
.card-head { display: flex; align-items: center; gap: 0.9rem; margin-bottom: 0.6rem; }
.icon-tile {
    width: 56px; height: 56px; min-width: 56px; border-radius: 18px;
    background: linear-gradient(150deg, #e4efff 0%, #bcd6ff 100%);
    display: flex; align-items: center; justify-content: center; font-size: 1.8rem;
    box-shadow: 0 6px 14px rgba(80, 130, 230, 0.2);
}
.card-title { font-size: 1.5rem; font-weight: 900; color: #2f5fcf; line-height: 1.25; word-break: keep-all; }
.card-sub { font-size: 1rem; color: #7a8bab; }

/* ---------- 버튼 ---------- */
.stApp button[kind="primary"], .stApp button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #4f8fff 0%, #78c0ff 100%);
    border: none; border-radius: 999px; min-height: 3.2rem;
    box-shadow: 0 8px 18px rgba(79, 143, 255, 0.35); transition: all 0.15s;
}
.stApp button[kind="primary"]:hover, .stApp button[kind="primaryFormSubmit"]:hover {
    transform: translateY(-2px); box-shadow: 0 10px 22px rgba(79, 143, 255, 0.45);
}
.stApp button[kind="primary"] p, .stApp button[kind="primaryFormSubmit"] p {
    color: #ffffff !important; font-size: 1.2rem !important; font-weight: 700;
}
.stApp button[kind="secondary"], .stApp button[kind="secondaryFormSubmit"] {
    background: #eef4ff; border: 2px solid #cfe0ff; border-radius: 999px; min-height: 3rem;
}
.stApp button[kind="secondary"] p, .stApp button[kind="secondaryFormSubmit"] p {
    color: #3b6fd8 !important; font-size: 1.1rem !important; font-weight: 700;
}

/* ---------- 입력창 ---------- */
.stApp [data-baseweb="input"], .stApp [data-baseweb="select"] > div {
    border-radius: 18px !important; background: #f3f7ff !important;
    border: 2px solid #d6e4ff !important; min-height: 3.1rem;
}
.stApp input { font-size: 1.2rem !important; color: #1e2a4a !important; }
.stApp [data-baseweb="select"] div { font-size: 1.15rem; color: #1e2a4a; }
.stApp label p { font-size: 1.1rem !important; font-weight: 700; color: #4a5b7c !important; }
[data-testid="stForm"] { border: none; padding: 0; }

/* ---------- 탭 ---------- */
.stTabs [role="tablist"] {
    gap: 0.3rem; background: #eef4ff; border-radius: 999px; padding: 0.35rem;
    border: none !important; box-shadow: none !important;
}
.stTabs [role="tab"] {
    border-radius: 999px; padding: 0.5rem 0.6rem; height: auto; flex: 1;
    display: flex; justify-content: center; border: none !important; background: transparent;
}
.stTabs [role="tab"] p { font-size: 1.15rem !important; font-weight: 700; color: #5a6b8c !important; }
.stTabs [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4f8fff, #78c0ff);
    box-shadow: 0 4px 12px rgba(79, 143, 255, 0.35);
}
.stTabs [role="tab"][aria-selected="true"] p { color: #ffffff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
/* ---------- 펼치기 상자 ---------- */
[data-testid="stExpander"] details {
    border-radius: 18px; border: 2px solid #dce8ff; background: #f7faff;
}
[data-testid="stExpander"] summary p { font-size: 1.15rem !important; font-weight: 700; color: #2f5fcf; }

/* ---------- 보기(라디오) ---------- */
.stRadio [role="radiogroup"] { gap: 0.55rem; }
.stRadio [role="radiogroup"] label {
    background: #f3f7ff; border: 2px solid #d6e4ff; border-radius: 18px;
    padding: 0.8rem 1.1rem; width: 100%; transition: all 0.15s;
}
.stRadio [role="radiogroup"] label:hover { border-color: #8fb8ff; }
.stRadio [role="radiogroup"] label:has(input:checked) { background: #dbe9ff; border-color: #4f8fff; }
.stRadio [role="radiogroup"] label p { font-size: 1.2rem !important; font-weight: 500; color: #1e2a4a !important; }

/* ---------- 번역 결과 ---------- */
.arrow-wrap { display: flex; justify-content: center; padding-top: 7.5rem; }
.arrow {
    width: 64px; height: 64px; border-radius: 50%;
    background: linear-gradient(135deg, #4f8fff, #78c0ff); color: #fff;
    display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 900;
    box-shadow: 0 8px 18px rgba(79, 143, 255, 0.4);
}
.ko-word {
    font-size: 3.3rem; font-weight: 900; line-height: 1.2; margin: 0.3rem 0 0.8rem;
    color: #2f5fcf;
}
.pill-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.8rem; }
.pill {
    background: #eef4ff; color: #2f5fcf; border-radius: 999px;
    padding: 0.45rem 1rem; font-size: 1.15rem; font-weight: 700;
}
.meaning { font-size: 1.2rem; margin-bottom: 0.6rem; }
.soft-box {
    background: #f3f7ff; border-radius: 18px; padding: 0.9rem 1.1rem;
    font-size: 1.2rem; margin: 0.6rem 0; color: #1e2a4a; line-height: 1.7;
}
.soft-box small { font-size: 1rem; color: #6a7b9b; }
.tip {
    background: #fff4d6; color: #4a3b00; border-radius: 18px;
    padding: 0.9rem 1.1rem; margin-top: 0.7rem; font-size: 1.12rem; line-height: 1.6;
}
.empty {
    text-align: center; color: #8a9bbb; font-size: 1.15rem; padding: 3rem 0.5rem;
}
.empty div { font-size: 3rem; margin-bottom: 0.4rem; }

/* ---------- 문제 ---------- */
.stat-row { display: flex; gap: 0.7rem; margin: 0.4rem 0 1rem; flex-wrap: wrap; }
.stat {
    flex: 1; min-width: 130px; border-radius: 20px; padding: 0.8rem 1rem;
    background: linear-gradient(150deg, #f0f6ff, #dbe9ff); text-align: center;
}
.stat b { display: block; font-size: 1.9rem; font-weight: 900; color: #2f5fcf; }
.stat span { font-size: 1rem; color: #5a6b8c; }
.q-chip {
    display: inline-block; background: #4f8fff; color: #fff; border-radius: 999px;
    padding: 0.3rem 0.9rem; font-size: 1rem; font-weight: 700; margin-right: 0.4rem;
}
.q-src { font-size: 1rem; color: #7a8bab; }
.q-text { font-size: 1.45rem; font-weight: 800; margin: 0.8rem 0; color: #1e2a4a; line-height: 1.5; }
.opt {
    border-radius: 18px; padding: 0.8rem 1.1rem; margin-bottom: 0.5rem;
    font-size: 1.2rem; border: 2px solid #e1eaff; background: #f7faff; color: #1e2a4a;
}
.opt.ok { background: #e3f8ec; border-color: #3cbf7a; font-weight: 700; }
.opt.no { background: #ffe9ec; border-color: #ff7b8c; text-decoration: line-through; }
.result-ok, .result-no {
    border-radius: 18px; padding: 1rem 1.2rem; font-size: 1.3rem; font-weight: 800; margin: 0.8rem 0 0.5rem;
}
.result-ok { background: linear-gradient(135deg, #dff7ea, #c8f0db); color: #1d7a4a; }
.result-no { background: linear-gradient(135deg, #ffe8eb, #ffd6dc); color: #b3263c; }

/* ---------- 한글 자모 타일 ---------- */
.sec-title { font-size: 1.2rem; font-weight: 800; color: #2f5fcf; margin: 0.9rem 0 0.5rem; }
.jamo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(70px, 1fr)); gap: 0.5rem; }
.jamo {
    background: linear-gradient(160deg, #f3f8ff, #dde9ff); border-radius: 16px;
    text-align: center; padding: 0.5rem 0.2rem; box-shadow: 0 3px 8px rgba(80, 130, 230, 0.1);
}
.jamo b { display: block; font-size: 1.9rem; color: #2f5fcf; line-height: 1.3; }
.jamo small { font-size: 0.85rem; color: #5a6b8c; }
.syllable {
    font-size: 5rem; font-weight: 900; text-align: center; color: #ffffff;
    background: linear-gradient(135deg, #4f8fff, #8fc3ff); border-radius: 24px;
    padding: 0.4rem 0; margin: 0.6rem 0; box-shadow: 0 10px 24px rgba(79, 143, 255, 0.35);
}
.ex-item {
    background: #f3f7ff; border-radius: 14px; padding: 0.6rem 0.9rem;
    margin-bottom: 0.45rem; font-size: 1.15rem;
}
.ex-item b { color: #2f5fcf; }
.footer { text-align: center; color: #7a8bab; font-size: 1.05rem; margin-top: 2rem; }
</style>
""",
    unsafe_allow_html=True,
)


def show_html(s):
    """여러 줄 HTML을 화면에 출력 (앞쪽 공백 때문에 코드블록이 되는 문제 방지)"""
    clean = "".join(line.strip() for line in s.splitlines())
    st.markdown(clean, unsafe_allow_html=True)


def esc(s):
    """AI가 만든 글자를 HTML에 안전하게 넣기"""
    return html.escape(str(s or "")).replace("\n", "<br>")


def bold_md(s):
    """**굵게** 표기를 <b>굵게</b>로 바꾸기"""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def card_head(icon, title, sub=""):
    show_html(f"""
        <div class="card-head">
            <div class="icon-tile">{icon}</div>
            <div><div class="card-title">{title}</div><div class="card-sub">{sub}</div></div>
        </div>""")


# ---------------------------------------------------------
# 데이터: 한글 자모
# ---------------------------------------------------------
CONSONANTS = [
    ("ㄱ", "기역", "g/k"), ("ㄴ", "니은", "n"), ("ㄷ", "디귿", "d/t"),
    ("ㄹ", "리을", "r/l"), ("ㅁ", "미음", "m"), ("ㅂ", "비읍", "b/p"),
    ("ㅅ", "시옷", "s"), ("ㅇ", "이응", "ng"), ("ㅈ", "지읒", "j"),
    ("ㅊ", "치읓", "ch"), ("ㅋ", "키읔", "k"), ("ㅌ", "티읕", "t"),
    ("ㅍ", "피읖", "p"), ("ㅎ", "히읗", "h"),
]
DOUBLE_CONSONANTS = [("ㄲ", "kk"), ("ㄸ", "tt"), ("ㅃ", "pp"), ("ㅆ", "ss"), ("ㅉ", "jj")]
VOWELS = [
    ("ㅏ", "a"), ("ㅑ", "ya"), ("ㅓ", "eo"), ("ㅕ", "yeo"), ("ㅗ", "o"),
    ("ㅛ", "yo"), ("ㅜ", "u"), ("ㅠ", "yu"), ("ㅡ", "eu"), ("ㅣ", "i"),
]

# 유니코드 한글 조합용 (순서 변경 금지)
CHO = ["ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
       "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
JUNG = ["ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ",
        "ㅚ", "ㅛ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ"]
JONG = ["(없음)", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ",
        "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ",
        "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]

# ---------------------------------------------------------
# 데이터: 문법
# ---------------------------------------------------------
GRAMMAR = {
    "은/는 (주제)": {
        "rule": "말하려는 주제를 나타내요. 받침 있으면 **은**, 없으면 **는**.",
        "examples": ["저**는** 학생이에요.", "한국**은** 겨울이 추워요."],
        "tip": "자기소개를 할 때 가장 많이 써요.",
    },
    "이/가 (주어)": {
        "rule": "문장의 주어(누가/무엇이)를 나타내요. 받침 있으면 **이**, 없으면 **가**.",
        "examples": ["비**가** 와요.", "가방**이** 무거워요."],
        "tip": "처음 말하는 새로운 정보에 자주 써요.",
    },
    "을/를 (목적어)": {
        "rule": "동작의 대상(무엇을)을 나타내요. 받침 있으면 **을**, 없으면 **를**.",
        "examples": ["밥**을** 먹어요.", "커피**를** 마셔요."],
        "tip": "말할 때는 자주 생략하기도 해요. (밥 먹어요)",
    },
    "에 / 에서 (장소)": {
        "rule": "**에**: 가다/오다/있다의 장소·시간. **에서**: 행동이 일어나는 장소.",
        "examples": ["학교**에** 가요.", "학교**에서** 공부해요.", "3시**에** 만나요."],
        "tip": "'어디에서 일해요?'처럼 행동이 있으면 '에서'!",
    },
    "-아요/-어요 (현재·존댓말)": {
        "rule": "일상에서 쓰는 부드러운 존댓말. ㅏ,ㅗ → **-아요**, 그 외 → **-어요**, 하다 → **해요**.",
        "examples": ["가다 → 가**요**", "먹다 → 먹**어요**", "공부하다 → 공부**해요**"],
        "tip": "처음 만난 사람, 직장, 가게에서는 이 말투가 가장 안전해요.",
    },
    "-았어요/-었어요 (과거)": {
        "rule": "지난 일을 말해요. ㅏ,ㅗ → **-았어요**, 그 외 → **-었어요**, 하다 → **했어요**.",
        "examples": ["어제 친구를 만**났어요**.", "점심을 먹**었어요**."],
        "tip": "'어제', '지난주' 같은 말과 함께 써요.",
    },
    "-(으)ㄹ 거예요 (미래)": {
        "rule": "앞으로 할 일, 계획을 말해요.",
        "examples": ["내일 병원에 **갈 거예요**.", "주말에 책을 **읽을 거예요**."],
        "tip": "받침이 있으면 '-을 거예요'.",
    },
    "-고 싶어요 (바람)": {
        "rule": "하고 싶은 것을 말해요.",
        "examples": ["김치찌개를 먹**고 싶어요**.", "한국어를 잘하**고 싶어요**."],
        "tip": "다른 사람의 바람은 '-고 싶어해요'.",
    },
    "-(으)세요 (부탁·안내)": {
        "rule": "공손하게 부탁하거나 안내할 때 써요.",
        "examples": ["여기 앉**으세요**.", "천천히 말해 주**세요**."],
        "tip": "'천천히 말해 주세요'는 꼭 외워 두세요!",
    },
    "안 / -지 않아요 (부정)": {
        "rule": "'아니다'의 뜻. 동사 앞에 **안**, 또는 뒤에 **-지 않아요**.",
        "examples": ["**안** 매워요.", "맵**지 않아요**."],
        "tip": "'못'은 '할 수 없다'는 뜻이에요. (못 먹어요)",
    },
}

# ---------------------------------------------------------
# 데이터: 문화 팁 (오해를 줄이기 위한 내용)
# ---------------------------------------------------------
CULTURE = [
    ("😊 나이를 물어봐요", "한국에서는 처음 만나면 나이를 자주 물어요. 무례한 것이 아니라 존댓말을 정하기 위해서예요.", "실례지만 나이가 어떻게 되세요?"),
    ("🍚 '밥 먹었어요?'", "실제로 밥을 먹었는지 궁금한 것이 아니라 '안녕하세요' 같은 인사예요.", "네, 먹었어요. ○○ 씨는요?"),
    ("🤝 '언제 밥 한번 먹어요'", "꼭 약속이 아니라 친해지고 싶다는 인사일 때가 많아요. 정말 만나려면 날짜를 정해 보세요.", "좋아요! 다음 주 금요일 어때요?"),
    ("🙌 두 손으로 주고받기", "어른이나 윗사람에게 물건을 줄 때는 두 손으로 줘요. 한 손을 쓰면 버릇없어 보일 수 있어요.", "여기 있습니다."),
    ("👟 신발 벗기", "집이나 일부 식당·병원 방에서는 신발을 벗어요. 입구에 신발이 있으면 벗으세요.", "신발 벗어야 해요?"),
    ("🖍️ 빨간색으로 이름 쓰기", "빨간색으로 사람 이름을 쓰는 것은 좋지 않게 생각해요.", "검은색 펜 있어요?"),
    ("👨‍👩‍👧 '우리'라는 말", "'우리 엄마', '우리 회사'처럼 '나의' 대신 '우리'를 많이 써요. 함께라는 느낌이에요.", "우리 회사는 천안에 있어요."),
    ("🙇 존댓말과 반말", "처음 만난 사람, 나이가 많은 사람에게는 존댓말(-요)을 써요. 반말은 친한 사이에서만!", "말 편하게 해도 될까요?"),
]

# ---------------------------------------------------------
# 데이터: API 키가 없을 때 쓰는 기본 사전
# (단어: 한국어, 로마자, 실제 발음, 뜻)
# ---------------------------------------------------------
FALLBACK_DICT = {
    "hello": ("안녕하세요", "annyeonghaseyo", "[안녕하세요]", "인사"),
    "thank you": ("감사합니다", "gamsahamnida", "[감사함니다]", "고마움 표현"),
    "thanks": ("고마워요", "gomawoyo", "[고마워요]", "고마움 표현"),
    "sorry": ("죄송합니다", "joesonghamnida", "[죄송함니다]", "사과"),
    "yes": ("네", "ne", "[네]", "대답"),
    "no": ("아니요", "aniyo", "[아니요]", "대답"),
    "water": ("물", "mul", "[물]", "마시는 물"),
    "rice": ("밥", "bap", "[밥]", "음식, 식사"),
    "hospital": ("병원", "byeongwon", "[병원]", "아플 때 가는 곳"),
    "pharmacy": ("약국", "yakguk", "[약꾹]", "약을 사는 곳"),
    "school": ("학교", "hakgyo", "[학꾜]", "공부하는 곳"),
    "friend": ("친구", "chingu", "[친구]", "친한 사람"),
    "family": ("가족", "gajok", "[가족]", "부모, 형제 등"),
    "work": ("일", "il", "[일]", "직업, 노동"),
    "money": ("돈", "don", "[돈]", "화폐"),
    "bus": ("버스", "beoseu", "[버스]", "교통수단"),
    "toilet": ("화장실", "hwajangsil", "[화장실]", "볼일 보는 곳"),
    "help": ("도와주세요", "dowajuseyo", "[도와주세요]", "도움 요청"),
    "teacher": ("선생님", "seonsaengnim", "[선생님]", "가르치는 사람"),
    "love": ("사랑", "sarang", "[사랑]", "사랑하는 마음"),
    "together": ("같이", "gachi", "[가치]", "함께"),
    "food": ("음식", "eumsik", "[음식]", "먹는 것"),
    "house": ("집", "jip", "[집]", "사는 곳"),
    "korea": ("한국", "hanguk", "[한국]", "나라 이름"),
}

# ---------------------------------------------------------
# 데이터: 기본 문제 (TOPIK I 스타일)
# answer = 정답 보기의 번호(0부터 시작). 화면에서는 보기 순서를 섞어서 보여줌.
# ---------------------------------------------------------
QUESTION_BANK = [
    {"category": "어휘", "passage": "사과가 있어요. 배도 있어요.",
     "question": "무엇에 대한 내용입니까?",
     "options": ["과일", "날씨", "직업", "가족"], "answer": 0,
     "explain": "사과와 배는 과일이에요."},
    {"category": "문법", "passage": "",
     "question": "(  )에 알맞은 것: 저는 학생(  ) 아니에요.",
     "options": ["이", "을", "에서", "와"], "answer": 0,
     "explain": "'○○이/가 아니에요'로 써요. 학생은 받침이 있어서 '이'."},
    {"category": "문법", "passage": "",
     "question": "(  )에 알맞은 것: 도서관(  ) 책을 읽어요.",
     "options": ["에서", "을", "이", "의"], "answer": 0,
     "explain": "책을 읽는 '행동'이 일어나는 장소라서 '에서'."},
    {"category": "문법", "passage": "",
     "question": "(  )에 알맞은 것: 어제 친구를 (  ).",
     "options": ["만났어요", "만나요", "만날 거예요", "만나세요"], "answer": 0,
     "explain": "'어제'는 과거라서 '-았어요'."},
    {"category": "어휘", "passage": "",
     "question": "'크다'의 반대말은 무엇입니까?",
     "options": ["작다", "많다", "길다", "높다"], "answer": 0,
     "explain": "크다 ↔ 작다"},
    {"category": "대화", "passage": "가: 이 사과 얼마예요?\n나: (        )",
     "question": "(  )에 알맞은 대답은 무엇입니까?",
     "options": ["세 개에 오천 원이에요.", "네, 맛있어요.", "시장에 가요.", "아니요, 괜찮아요."],
     "answer": 0, "explain": "'얼마예요?'는 가격을 묻는 말이에요."},
    {"category": "읽기",
     "passage": "저는 베트남에서 왔습니다. 한국에 온 지 1년이 되었습니다. 지금 공장에서 일합니다. 주말에는 한국어를 배웁니다.",
     "question": "내용과 같은 것을 고르십시오.",
     "options": ["저는 주말에 한국어를 공부합니다.", "저는 한국에서 태어났습니다.",
                 "저는 학교에서 일합니다.", "한국에 온 지 3년이 되었습니다."],
     "answer": 0, "explain": "'주말에는 한국어를 배웁니다'와 같은 뜻이에요."},
    {"category": "존댓말", "passage": "",
     "question": "할머니께 알맞게 말한 것은? '할머니, 진지 (  )?'",
     "options": ["드셨어요", "먹었어", "먹어", "먹자"], "answer": 0,
     "explain": "어른에게는 '먹다' 대신 '드시다', '밥' 대신 '진지'를 써요."},
    {"category": "어휘", "passage": "",
     "question": "(  )에 알맞은 것: 비가 와요. 그래서 (  )을 가지고 가요.",
     "options": ["우산", "안경", "지갑", "모자"], "answer": 0,
     "explain": "비가 올 때는 우산이 필요해요."},
    {"category": "어휘", "passage": "",
     "question": "약을 사고 싶어요. 어디에 가요?",
     "options": ["약국", "은행", "우체국", "서점"], "answer": 0,
     "explain": "약은 약국에서 사요."},
    {"category": "문법", "passage": "",
     "question": "(  )에 알맞은 것: 주말에 영화를 (  ) 싶어요.",
     "options": ["보고", "보면", "봐서", "보는"], "answer": 0,
     "explain": "바람을 말할 때 '-고 싶어요'."},
    {"category": "대화", "passage": "가: 처음 뵙겠습니다.\n나: (        )",
     "question": "(  )에 알맞은 대답은 무엇입니까?",
     "options": ["반갑습니다.", "안녕히 가세요.", "잘 먹겠습니다.", "죄송합니다."],
     "answer": 0, "explain": "처음 만났을 때는 '반갑습니다'라고 해요."},
    {"category": "문화", "passage": "가: 밥 먹었어요?\n나: (        )",
     "question": "이 말에 가장 자연스러운 대답은?",
     "options": ["네, 먹었어요. ○○ 씨는요?", "왜 물어봐요?", "그건 비밀이에요.", "밥을 사 주세요."],
     "answer": 0, "explain": "'밥 먹었어요?'는 인사예요. 가볍게 대답하면 돼요."},
]

LANGUAGES = ["자동 감지", "English", "中文", "Tiếng Việt", "日本語", "ไทย",
             "Русский", "Bahasa Indonesia", "Filipino", "Монгол", "Oʻzbekcha",
             "Español", "Français", "नेपाली"]

# ---------------------------------------------------------
# 세션 상태 초기화
# ---------------------------------------------------------
def init_state():
    defaults = {
        "translation": None,
        "translation_error": None,
        "quiz_order": random.sample(range(len(QUESTION_BANK)), len(QUESTION_BANK)),
        "quiz_pos": 0,
        "current_q": None,
        "q_serial": 0,
        "answered": False,
        "last_choice": None,
        "score": 0,
        "total": 0,
        "quiz_error": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ---------------------------------------------------------
# AI 관련 함수
# ---------------------------------------------------------
def get_client():
    """GEMINI_API_KEY가 있으면 클라이언트 반환, 없으면 None"""
    if not GENAI_OK:
        return None
    try:
        key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception:
        return None


def friendly_error(e):
    msg = str(e)
    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
        return "요청이 너무 많아요. 1분 정도 기다렸다가 다시 시도해 주세요."
    if "API_KEY_INVALID" in msg or "API key" in msg or "401" in msg or "403" in msg:
        return "API 키가 올바르지 않아요. Secrets의 GEMINI_API_KEY를 확인해 주세요."
    if "503" in msg or "UNAVAILABLE" in msg or "overloaded" in msg:
        return "AI 서버가 바빠요. 잠시 후 다시 시도해 주세요."
    return "AI 응답 중 오류가 발생했어요: " + msg[:150]


def parse_json(text):
    """AI 응답에서 JSON 부분만 꺼내서 dict로 변환"""
    if not text:
        raise ValueError("빈 응답")
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("JSON 형식이 아님")
    return json.loads(text[start:end + 1])


def ask_gemini_json(prompt):
    client = get_client()
    if client is None:
        raise RuntimeError("NO_KEY")
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.4,
        ),
    )
    return parse_json(response.text)


TRANSLATE_PROMPT = """
너는 한국에 사는 이주민에게 한국어를 가르치는 친절한 선생님이야.
입력: "<<WORD>>"
입력 언어: <<LANG>>
이 단어(또는 문장)를 자연스러운 한국어로 번역하고, 아래 JSON 형식으로만 답해.
{
  "korean": "한국어 번역",
  "romanization": "로마자 표기 (국립국어원 표기법)",
  "pronunciation": "실제로 소리 나는 대로 쓴 한글 발음 (예: 같이 → [가치])",
  "meaning": "입력 언어로 쓴 짧은 뜻 설명",
  "example_ko": "이 말을 사용한 쉬운 한국어 예문 1개",
  "example_native": "예문을 입력 언어로 번역한 것",
  "culture_tip": "이 표현을 한국에서 쓸 때 문화적으로 주의할 점(오해 방지)이 있으면 쉬운 한국어로 1~2문장, 없으면 빈 문자열"
}
"""

QUIZ_PROMPT = """
너는 한국어능력시험(TOPIK) 출제 위원이야.
수준: <<LEVEL>>
문제 유형: <<TYPE>>
한국에 사는 이주민의 실제 생활(직장, 병원, 시장, 이웃, 관공서, 학교 등)과 관련된 4지선다 문제 1개를 만들어.
아래 JSON 형식으로만 답해.
{
  "category": "문제 유형",
  "passage": "지문이나 대화 (없으면 빈 문자열)",
  "question": "문제",
  "options": ["보기1", "보기2", "보기3", "보기4"],
  "answer": 정답 보기의 번호(0~3 정수),
  "explain": "쉬운 한국어로 쓴 해설 1~2문장"
}
"""


def translate_word(word, lang):
    """번역 결과(dict)와 오류 메시지(str 또는 None)를 반환"""
    if get_client() is None:
        key = word.strip().lower()
        if key in FALLBACK_DICT:
            ko, rom, pron, meaning = FALLBACK_DICT[key]
            return {"korean": ko, "romanization": rom, "pronunciation": pron,
                    "meaning": meaning, "example_ko": "", "example_native": "",
                    "culture_tip": ""}, None
        return None, ("AI 키가 설정되지 않아 기본 사전만 사용 중이에요. "
                      "기본 사전 단어: " + ", ".join(list(FALLBACK_DICT.keys())[:12]) + " …")

    lang_text = "입력 언어를 스스로 판단해" if lang == "자동 감지" else lang
    prompt = TRANSLATE_PROMPT.replace("<<WORD>>", word).replace("<<LANG>>", lang_text)
    try:
        data = ask_gemini_json(prompt)
        if not isinstance(data, dict) or not data.get("korean"):
            return None, "번역 결과를 이해하지 못했어요. 다시 시도해 주세요."
        return data, None
    except Exception as e:
        return None, friendly_error(e)


# ---------------------------------------------------------
# 발음 듣기 (gTTS)
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def make_audio(text):
    if not GTTS_OK or not text:
        return None
    try:
        buf = io.BytesIO()
        gTTS(text=text, lang="ko").write_to_fp(buf)
        return buf.getvalue()
    except Exception:
        return None


def play_audio(text):
    audio = make_audio(text)
    if audio:
        st.audio(audio, format="audio/mp3")
    else:
        st.caption("🔇 지금은 소리를 만들 수 없어요. (인터넷 연결 확인)")


# ---------------------------------------------------------
# 퀴즈 관련 함수
# ---------------------------------------------------------
def set_question(q, source):
    options = list(q["options"])
    correct = options[q["answer"]]
    random.shuffle(options)
    st.session_state.q_serial += 1
    st.session_state.current_q = {
        "id": st.session_state.q_serial,
        "category": q.get("category", ""),
        "passage": q.get("passage", ""),
        "question": q.get("question", ""),
        "options": options,
        "correct": correct,
        "explain": q.get("explain", ""),
        "source": source,
    }
    st.session_state.answered = False
    st.session_state.last_choice = None


def load_bank_question():
    st.session_state.quiz_error = None
    pos = st.session_state.quiz_pos
    if pos >= len(st.session_state.quiz_order):
        st.session_state.quiz_order = random.sample(range(len(QUESTION_BANK)), len(QUESTION_BANK))
        pos = 0
    q = QUESTION_BANK[st.session_state.quiz_order[pos]]
    st.session_state.quiz_pos = pos + 1
    set_question(q, "기본 문제")


def load_ai_question():
    st.session_state.quiz_error = None
    if get_client() is None:
        st.session_state.quiz_error = "AI 문제를 만들려면 GEMINI_API_KEY가 필요해요. 기본 문제를 풀어 보세요!"
        return
    level = st.session_state.get("ai_level", "TOPIK I (1~2급)")
    qtype = st.session_state.get("ai_type", "어휘")
    prompt = QUIZ_PROMPT.replace("<<LEVEL>>", level).replace("<<TYPE>>", qtype)
    try:
        data = ask_gemini_json(prompt)
        options = data.get("options")
        answer = int(data.get("answer"))
        if (not isinstance(options, list) or len(options) != 4
                or not 0 <= answer <= 3 or not data.get("question")):
            raise ValueError("문제 형식 오류")
        data["options"] = [str(o) for o in options]
        data["answer"] = answer
        set_question(data, "AI 문제 · " + level)
    except ValueError:
        st.session_state.quiz_error = "AI가 만든 문제 형식이 올바르지 않아요. 다시 눌러 주세요."
    except Exception as e:
        st.session_state.quiz_error = friendly_error(e)


def reset_score():
    st.session_state.score = 0
    st.session_state.total = 0


# =========================================================
# 화면 그리기
# =========================================================
init_state()
if st.session_state.current_q is None:
    load_bank_question()

# ---------------- 상단 배너 ----------------
show_html("""
<div class="hero">
    <div class="hero-top">
        <div class="avatar">🙂</div>
        <div class="hello">안녕하세요! 👋<br><small>Welcome to Korea</small></div>
        <div class="bell">🔔</div>
    </div>
    <div class="hero-title">듀오RINGGO</div>
    <div class="hero-sub">한국어와 한국 문화를 함께 배우고, 오해 없이 소통해요</div>
    <div class="chips"><span>🌍 번역 · 발음</span><span>📝 TOPIK 문제</span><span>📚 문법 · 문화</span></div>
</div>
""")

if get_client() is None:
    st.info("AI 키가 없어 기본 사전과 기본 문제로 작동 중이에요. 배포 후 Secrets에 GEMINI_API_KEY를 넣으면 AI 기능이 켜져요.")

left, right = st.columns([2.5, 1], gap="large")

# ---------------- 왼쪽 ----------------
with left:
    c_in, c_arrow, c_out = st.columns([5, 1, 5])

    # 1) 다른 언어 입력
    with c_in:
        with st.container(key="card_input"):
            card_head("🌍", "다른 언어", "My language")
            with st.form("translate_form", border=False):
                lang = st.selectbox("내 언어", LANGUAGES)
                word = st.text_input("단어나 짧은 문장", placeholder="예: hello, together, 谢谢")
                go = st.form_submit_button("한국어로 바꾸기", type="primary", width="stretch")
            if go:
                if not word.strip():
                    st.warning("단어를 입력해 주세요.")
                elif len(word) > 200:
                    st.warning("200자 이내로 입력해 주세요.")
                else:
                    with st.spinner("번역 중..."):
                        result, err = translate_word(word.strip(), lang)
                    st.session_state.translation = result
                    st.session_state.translation_error = err

    with c_arrow:
        show_html('<div class="arrow-wrap"><div class="arrow">➜</div></div>')

    # 2) 번역된 한국어 + 발음
    with c_out:
        with st.container(key="card_output"):
            card_head("🇰🇷", "번역된 한국어", "Korean")
            tr = st.session_state.translation
            if st.session_state.translation_error:
                st.warning(st.session_state.translation_error)
            if tr:
                show_html(f"""
                    <div class="ko-word">{esc(tr.get("korean"))}</div>
                    <div class="pill-row">
                        <span class="pill">🔤 {esc(tr.get("romanization"))}</span>
                        <span class="pill">🗣️ {esc(tr.get("pronunciation"))}</span>
                    </div>""")
                if tr.get("meaning"):
                    show_html(f'<div class="meaning">📖 <b>뜻</b> · {esc(tr.get("meaning"))}</div>')
                play_audio(tr.get("korean", ""))
                if tr.get("example_ko"):
                    native = f'<br><small>{esc(tr.get("example_native"))}</small>' if tr.get("example_native") else ""
                    show_html(f'<div class="soft-box">✏️ <b>예문</b><br>{esc(tr.get("example_ko"))}{native}</div>')
                    if st.button("🔊 예문 듣기", width="stretch"):
                        play_audio(tr.get("example_ko"))
                if tr.get("culture_tip"):
                    show_html(f'<div class="tip">💡 <b>문화 팁</b><br>{esc(tr.get("culture_tip"))}</div>')
            elif not st.session_state.translation_error:
                show_html('<div class="empty"><div>💬</div>왼쪽에 단어를 넣으면<br>한국어 뜻과 발음이 나와요</div>')

    st.write("")

    # 3) 한국어 문제
    with st.container(key="card_quiz"):
        card_head("📝", "한국어 문제", "TOPIK 스타일 · 실생활 한국어")

        total = st.session_state.total
        score = st.session_state.score
        rate = (score / total * 100) if total else 0
        show_html(f"""
            <div class="stat-row">
                <div class="stat"><b>{score}</b><span>맞힌 문제</span></div>
                <div class="stat"><b>{total}</b><span>푼 문제</span></div>
                <div class="stat"><b>{rate:.0f}%</b><span>정답률</span></div>
            </div>""")

        with st.expander("✨ AI로 새 문제 만들기"):
            a1, a2 = st.columns(2)
            a1.selectbox("수준", ["TOPIK I (1~2급)", "TOPIK II (3~4급)"], key="ai_level")
            a2.selectbox("유형", ["어휘", "문법", "읽기", "대화 완성", "존댓말", "한국 생활 문화"], key="ai_type")
            st.button("AI 문제 만들기", on_click=load_ai_question, type="primary", width="stretch")

        if st.session_state.quiz_error:
            st.warning(st.session_state.quiz_error)

        q = st.session_state.current_q
        show_html(f'<span class="q-chip">{esc(q["category"])}</span><span class="q-src">{esc(q["source"])}</span>')
        if q["passage"]:
            show_html(f'<div class="soft-box">{esc(q["passage"])}</div>')
        show_html(f'<div class="q-text">{esc(q["question"])}</div>')

        if not st.session_state.answered:
            with st.form(f"quiz_form_{q['id']}", border=False):
                choice = st.radio("정답을 고르세요", q["options"], index=None,
                                  key=f"choice_{q['id']}", label_visibility="collapsed")
                submitted = st.form_submit_button("정답 확인", type="primary", width="stretch")
            if submitted:
                if choice is None:
                    st.warning("보기를 하나 골라 주세요.")
                else:
                    st.session_state.answered = True
                    st.session_state.last_choice = choice
                    st.session_state.total += 1
                    if choice == q["correct"]:
                        st.session_state.score += 1
                    st.rerun()
        else:
            rows = ""
            for opt in q["options"]:
                if opt == q["correct"]:
                    rows += f'<div class="opt ok">✅ {esc(opt)}</div>'
                elif opt == st.session_state.last_choice:
                    rows += f'<div class="opt no">❌ {esc(opt)}</div>'
                else:
                    rows += f'<div class="opt">{esc(opt)}</div>'
            show_html(rows)
            if st.session_state.last_choice == q["correct"]:
                show_html('<div class="result-ok">🎉 정답이에요! 잘했어요</div>')
            else:
                show_html(f'<div class="result-no">😢 아쉬워요. 정답은 \'{esc(q["correct"])}\' 이에요</div>')
            if q["explain"]:
                show_html(f'<div class="soft-box">💬 <b>해설</b> · {esc(q["explain"])}</div>')

        b1, b2 = st.columns([2, 1])
        b1.button("다음 문제 ➜", on_click=load_bank_question, type="primary", width="stretch")
        b2.button("점수 초기화", on_click=reset_score, width="stretch")

# ---------------- 오른쪽: 한국어 문법, 사용법 ----------------
with right:
    with st.container(key="card_grammar"):
        card_head("📚", "한국어 문법, 사용법", "Hangul · Grammar · Culture")
        tab1, tab2, tab3 = st.tabs(["한글", "문법", "문화"])

        with tab1:
            show_html('<div class="sec-title">자음 Consonants</div><div class="jamo-grid">'
                      + "".join(f'<div class="jamo"><b>{c}</b><small>{n} · {s}</small></div>'
                                for c, n, s in CONSONANTS)
                      + "</div>")
            show_html('<div class="sec-title">쌍자음</div><div class="jamo-grid">'
                      + "".join(f'<div class="jamo"><b>{c}</b><small>{s}</small></div>'
                                for c, s in DOUBLE_CONSONANTS)
                      + "</div>")
            show_html('<div class="sec-title">모음 Vowels</div><div class="jamo-grid">'
                      + "".join(f'<div class="jamo"><b>{v}</b><small>{s}</small></div>'
                                for v, s in VOWELS)
                      + "</div>")
            show_html('<div class="sec-title">🧩 글자 만들기</div>')
            cho = st.selectbox("첫소리 (자음)", CHO, index=11)
            jung = st.selectbox("가운뎃소리 (모음)", JUNG, index=0)
            jong = st.selectbox("끝소리 (받침)", JONG, index=0)
            code = 0xAC00 + (CHO.index(cho) * 21 + JUNG.index(jung)) * 28 + JONG.index(jong)
            syllable = chr(code)
            show_html(f'<div class="syllable">{syllable}</div>')
            if st.button("🔊 소리 듣기", type="primary", width="stretch"):
                play_audio(syllable)

        with tab2:
            g = st.selectbox("문법 고르기", list(GRAMMAR.keys()))
            item = GRAMMAR[g]
            show_html(f'<div class="soft-box">{bold_md(item["rule"])}</div>')
            show_html('<div class="sec-title">예문</div>'
                      + "".join(f'<div class="ex-item">{bold_md(ex)}</div>' for ex in item["examples"]))
            show_html(f'<div class="tip">💡 {item["tip"]}</div>')

        with tab3:
            show_html('<div class="soft-box">한국 생활에서 생길 수 있는<br><b>오해를 줄여요</b> 🤝</div>')
            for title, desc, phrase in CULTURE:
                with st.expander(title):
                    st.write(desc)
                    show_html(f'<div class="ex-item">🗨️ <b>{phrase}</b></div>')

show_html('<div class="footer">듀오RINGGO · 언어와 문화의 차이를 이해하면 오해가 줄어요 🤝</div>')
