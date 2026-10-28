import io
import re
import hashlib

import streamlit as st
from gtts import gTTS
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(page_title="버스 번호 인식", page_icon="🚌", layout="centered")

MODEL_NAME = "gemini-2.5-flash-lite"
FAIL_MESSAGE = "버스 번호를 인식하지 못했습니다. 버스 앞쪽 번호판을 향해 카메라를 다시 비춰주세요."

# ---------------------------------------------------------
# 디자인 (딥 그린 + 골드 + 베이지)
# ---------------------------------------------------------
st.markdown(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Noto+Serif+KR:wght@700;900&family=Playfair+Display:wght@700;800&display=swap');

:root {
  --green: #1F5A48;
  --green-dark: #163F33;
  --gold: #9A7440;
  --gold-light: #C9A46B;
  --beige: #F4EFE6;
  --ink: #1E1E1E;
}

html, body, [class*="css"], .stApp {
  font-family: 'Noto Sans KR', sans-serif;
  color: var(--ink);
}
.stApp { background-color: #FFFFFF; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 760px; }
header[data-testid="stHeader"] { background: transparent; }

/* 상단 내비게이션 */
.topbar { display:flex; justify-content:space-between; align-items:center; padding:6px 4px 10px 4px; }
.logo { font-family:'Playfair Display', serif; font-size:1.6rem; font-weight:800; color:var(--green); letter-spacing:1px; }
.logo span { color:var(--gold); }
.top-badge { background:var(--gold); color:#fff; font-size:0.85rem; font-weight:700; padding:6px 14px; border-radius:4px; }
.menubar { background:var(--green); color:#fff; display:flex; justify-content:center; gap:28px; padding:10px 0; font-size:0.95rem; font-weight:700; border-radius:2px; }

/* 히어로 배너 */
.hero { margin-top:14px; padding:46px 30px; border-radius:4px; color:#fff;
  background: linear-gradient(120deg, rgba(22,63,51,0.96) 0%, rgba(31,90,72,0.90) 55%, rgba(154,116,64,0.85) 100%); }
.hero-en { font-family:'Playfair Display', serif; font-size:2.3rem; font-weight:800; line-height:1.15; letter-spacing:1px; }
.hero-line { width:50px; height:3px; background:var(--gold-light); margin:16px 0; }
.hero-ko { font-size:1.25rem; font-weight:500; line-height:1.6; }

/* 섹션 제목 */
.sec-label { text-align:center; color:var(--gold); font-size:0.85rem; font-weight:700; letter-spacing:3px; margin-top:34px; }
.sec-title { text-align:center; font-family:'Noto Serif KR', serif; font-size:1.8rem; font-weight:900; color:var(--ink); margin:4px 0 4px 0; }
.sec-bar { width:36px; height:3px; background:var(--gold); margin:10px auto 18px auto; }

/* 이용 방법 (베이지 + 원형 아이콘) */
.how-wrap { background:var(--beige); padding:26px 14px; border-radius:4px; display:flex; gap:12px; justify-content:space-between; }
.how-card { flex:1; text-align:center; }
.how-icon { width:78px; height:78px; border-radius:50%; background:var(--green); color:#fff; display:flex; align-items:center; justify-content:center; font-size:2.1rem; margin:0 auto 10px auto; border:4px solid #fff; box-shadow:0 0 0 2px var(--green); }
.how-step { color:var(--gold); font-weight:900; font-size:0.85rem; }
.how-text { font-weight:700; font-size:1.05rem; }

/* 입력창 */
.stTextInput label p { font-size:1.15rem !important; font-weight:700 !important; color:var(--green) !important; }
.stTextInput input { font-size:1.4rem !important; border:2px solid var(--green) !important; border-radius:4px !important; padding:12px !important; }

/* 카메라 영역 */
[data-testid="stCameraInput"] { border:2px solid var(--green); border-radius:4px; padding:8px; background:#fff; }
[data-testid="stCameraInput"] button { background:var(--green) !important; color:#fff !important; font-size:1.2rem !important; font-weight:700 !important; }
.cam-guide { text-align:center; background:var(--green); color:#fff; font-size:1.35rem; font-weight:800; padding:12px; border-radius:4px 4px 0 0; }

/* 결과 영역 (그린 상담 블록 느낌) */
.result-box { background:var(--green); color:#fff; padding:30px 22px; border-radius:4px; margin:18px 0 10px 0; border-left:8px solid var(--gold-light); }
.result-label { color:var(--gold-light); font-size:0.9rem; font-weight:700; letter-spacing:3px; }
.result-text { font-family:'Noto Serif KR', serif; font-size:2.2rem; font-weight:900; line-height:1.4; margin-top:6px; }
.fail-box { background:#FFF3F0; color:#A3241A; padding:24px 20px; border-radius:4px; margin:18px 0 10px 0; border-left:8px solid #A3241A; font-size:1.35rem; font-weight:800; line-height:1.5; }

/* 골드 버튼 */
div.stButton > button { width:100%; height:68px; background:var(--gold); color:#fff; border:none; border-radius:4px; font-size:1.45rem; font-weight:800; }
div.stButton > button:hover { background:var(--green); color:#fff; }
div.stButton > button:focus { outline:4px solid var(--gold-light); color:#fff; }

/* 푸터 */
.footer { background:#222; color:#cfcfcf; padding:20px; border-radius:4px; margin-top:30px; font-size:0.9rem; line-height:1.7; }
.footer b { color:var(--gold-light); font-family:'Playfair Display', serif; font-size:1.1rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 세션 상태 초기화
# ---------------------------------------------------------
if "camera_key" not in st.session_state:
    st.session_state.camera_key = 0
if "last_hash" not in st.session_state:
    st.session_state.last_hash = None
if "result" not in st.session_state:
    st.session_state.result = None


# ---------------------------------------------------------
# 함수 정의
# ---------------------------------------------------------
def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


def parse_bus_number(text):
    if not text:
        return None
    first_line = text.strip().splitlines()[0].strip()
    first_line = first_line.replace("번", "").replace("버스", "").strip()
    if first_line.upper() in ("NONE", "없음", ""):
        return None
    if len(first_line) > 10:
        return None
    if not re.search(r"\d", first_line):
        return None
    return first_line


def recognize_bus_number(client, image_bytes, mime_type):
    prompt = (
        "이 사진은 시각장애인이 정류장에서 다가오는 버스를 촬영한 것입니다.\n"
        "버스 앞면, 옆면, 전광판에 표시된 '버스 노선 번호'만 찾아주세요.\n"
        "규칙:\n"
        "1. 노선 번호만 그대로 한 줄로 답하세요. 예: 14, 720-1, 마을2, 급행5\n"
        "2. 차량 번호판(예: 12가3456)은 노선 번호가 아니므로 무시하세요.\n"
        "3. 버스가 없거나 번호가 흐려서 확실하지 않으면 NONE 이라고만 답하세요.\n"
        "4. 설명, 문장, 따옴표 없이 답만 쓰세요."
    )
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), prompt],
    )
    try:
        text = response.text
    except Exception:
        text = None
    return parse_bus_number(text)


@st.cache_data(show_spinner=False)
def make_speech(text):
    fp = io.BytesIO()
    gTTS(text=text, lang="ko").write_to_fp(fp)
    return fp.getvalue()


def speak(text):
    try:
        audio = make_speech(text)
        st.audio(audio, format="audio/mp3", autoplay=True)
        st.caption("🔊 소리가 나지 않으면 위 재생 버튼을 눌러주세요.")
    except Exception:
        st.warning("음성을 만들지 못했습니다. 화면의 글자를 확인해주세요.")


def build_message(number, target):
    message = f"{number}번 버스입니다."
    if target:
        if number.replace(" ", "") == target.replace(" ", ""):
            message += " 기다리시던 버스가 도착했습니다. 탑승하세요."
        else:
            message += f" 기다리시는 {target}번 버스가 아닙니다."
    return message


def error_message(e):
    msg = str(e)
    if "429" in msg or "quota" in msg.lower() or "RESOURCE_EXHAUSTED" in msg:
        return "AI 사용량이 잠시 초과되었습니다. 1분 뒤 다시 시도해주세요."
    if "API key" in msg or "401" in msg or "403" in msg or "PERMISSION" in msg:
        return "API 키가 올바르지 않습니다. Secrets의 GEMINI_API_KEY를 확인해주세요."
    return "AI 연결 중 문제가 생겼습니다. 잠시 후 다시 인식해주세요."


# ---------------------------------------------------------
# 상단 + 히어로
# ---------------------------------------------------------
st.markdown(
    '<div class="topbar"><div class="logo">🚌 BUS<span>VOICE</span></div>'
    '<div class="top-badge">음성 안내 서비스</div></div>'
    '<div class="menubar"><span>버스 인식</span><span>이용 방법</span><span>음성 안내</span></div>'
    '<div class="hero"><div class="hero-en">YOUR BUS,<br>YOUR VOICE</div>'
    '<div class="hero-line"></div>'
    '<div class="hero-ko">카메라로 버스를 비추면<br>몇 번 버스인지 소리로 알려드립니다.</div></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 이용 방법
# ---------------------------------------------------------
st.markdown(
    '<div class="sec-label">HOW TO USE</div>'
    '<div class="sec-title">이용 방법</div><div class="sec-bar"></div>'
    '<div class="how-wrap">'
    '<div class="how-card"><div class="how-icon">📷</div><div class="how-step">STEP 01</div><div class="how-text">버스 비추기</div></div>'
    '<div class="how-card"><div class="how-icon">🔍</div><div class="how-step">STEP 02</div><div class="how-text">번호 인식</div></div>'
    '<div class="how-card"><div class="how-icon">🔊</div><div class="how-step">STEP 03</div><div class="how-text">음성 안내</div></div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# API 준비
# ---------------------------------------------------------
api_key = get_api_key()
if not api_key:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다. 배포 설정의 Secrets에 키를 넣어주세요.")
    st.stop()

try:
    client = get_client(api_key)
except Exception:
    st.error("AI를 준비하지 못했습니다. API 키를 확인해주세요.")
    st.stop()

# ---------------------------------------------------------
# 버스 인식 섹션
# ---------------------------------------------------------
st.markdown(
    '<div class="sec-label">BUS RECOGNITION</div>'
    '<div class="sec-title">버스 번호 인식</div><div class="sec-bar"></div>',
    unsafe_allow_html=True,
)

target_bus = st.text_input(
    "기다리는 버스 번호 (선택)",
    placeholder="예: 14",
    help="입력하면 도착한 버스가 맞는지 함께 알려드립니다.",
).strip()

st.markdown('<div class="cam-guide">📷 버스를 비춰주세요</div>', unsafe_allow_html=True)

photo = st.camera_input(
    "카메라 촬영",
    key=f"camera_{st.session_state.camera_key}",
    label_visibility="collapsed",
)

with st.expander("카메라가 열리지 않나요? 사진 올리기"):
    uploaded = st.file_uploader(
        "버스 사진 선택",
        type=["jpg", "jpeg", "png"],
        key=f"upload_{st.session_state.camera_key}",
    )

image_file = photo if photo is not None else uploaded

# ---------------------------------------------------------
# 인식 처리
# ---------------------------------------------------------
if image_file is not None:
    try:
        image_bytes = image_file.getvalue()
        mime_type = image_file.type if image_file.type else "image/jpeg"
        image_hash = hashlib.md5(image_bytes + target_bus.encode()).hexdigest()

        if image_hash != st.session_state.last_hash:
            with st.spinner("버스 번호를 읽고 있습니다..."):
                try:
                    number = recognize_bus_number(client, image_bytes, mime_type)
                    if number:
                        st.session_state.result = {"ok": True, "message": build_message(number, target_bus)}
                    else:
                        st.session_state.result = {"ok": False, "message": FAIL_MESSAGE}
                except Exception as e:
                    st.session_state.result = {"ok": False, "message": error_message(e)}
            st.session_state.last_hash = image_hash
    except Exception:
        st.session_state.result = {"ok": False, "message": "사진을 읽지 못했습니다. 다시 촬영해주세요."}

# ---------------------------------------------------------
# 결과 표시 + 음성
# ---------------------------------------------------------
result = st.session_state.result
if result:
    if result["ok"]:
        st.markdown(
            f'<div class="result-box"><div class="result-label">RESULT</div>'
            f'<div class="result-text">🔊 {result["message"]}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f'<div class="fail-box">⚠️ {result["message"]}</div>', unsafe_allow_html=True)
    speak(result["message"])

# ---------------------------------------------------------
# 다시 인식하기
# ---------------------------------------------------------
if st.button("🔄 다시 인식하기"):
    st.session_state.camera_key += 1
    st.session_state.last_hash = None
    st.session_state.result = None
    st.rerun()

# ---------------------------------------------------------
# 푸터
# ---------------------------------------------------------
st.markdown(
    '<div class="footer"><b>BUS VOICE</b><br>'
    '시각장애인의 안전한 버스 탑승을 돕는 음성 안내 서비스<br>'
    '※ AI 인식은 틀릴 수 있습니다. 탑승 전 기사님께 한 번 더 확인하세요.</div>',
    unsafe_allow_html=True,
)
