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
# 화면 디자인 (큰 글씨, 고대비)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .title-box {
        border: 3px solid #1f3b73; border-radius: 16px;
        padding: 14px; text-align: center;
        font-size: 2rem; font-weight: 800;
        background-color: #ffffff; color: #1f3b73;
        margin-bottom: 10px;
    }
    .guide-text {
        font-size: 1.4rem; font-weight: 700; text-align: center;
        color: #1f3b73; margin: 8px 0;
    }
    .result-box {
        border: 3px solid #1f3b73; border-radius: 16px;
        padding: 22px; text-align: center;
        font-size: 2.2rem; font-weight: 900;
        background-color: #fff8d6; color: #000000;
        margin: 12px 0;
    }
    .fail-box {
        border: 3px solid #b00020; border-radius: 16px;
        padding: 18px; text-align: center;
        font-size: 1.4rem; font-weight: 800;
        background-color: #ffe5e5; color: #b00020;
        margin: 12px 0;
    }
    div.stButton > button {
        width: 100%; height: 70px;
        font-size: 1.5rem; font-weight: 800;
        border-radius: 14px;
    }
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
    st.session_state.result = None  # {"ok": bool, "number": str, "message": str}


# ---------------------------------------------------------
# 함수 정의
# ---------------------------------------------------------
def get_api_key():
    """Secrets에서 API 키를 안전하게 가져온다."""
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return None


@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


def parse_bus_number(text):
    """AI 응답에서 버스 번호만 깔끔하게 꺼낸다."""
    if not text:
        return None
    first_line = text.strip().splitlines()[0].strip()
    first_line = first_line.replace("번", "").replace("버스", "").strip()

    if first_line.upper() in ("NONE", "없음", ""):
        return None
    if len(first_line) > 10:          # 너무 길면 번호가 아님
        return None
    if not re.search(r"\d", first_line):  # 숫자가 하나도 없으면 실패
        return None
    return first_line


def recognize_bus_number(client, image_bytes, mime_type):
    """Gemini로 사진 속 버스 번호를 인식한다."""
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
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt,
        ],
    )
    try:
        text = response.text
    except Exception:
        text = None
    return parse_bus_number(text)


@st.cache_data(show_spinner=False)
def make_speech(text):
    """문장을 한국어 음성(mp3)으로 만든다."""
    fp = io.BytesIO()
    gTTS(text=text, lang="ko").write_to_fp(fp)
    return fp.getvalue()


def speak(text):
    """음성을 자동 재생한다. 실패해도 앱은 멈추지 않는다."""
    try:
        audio = make_speech(text)
        st.audio(audio, format="audio/mp3", autoplay=True)
        st.caption("🔊 소리가 나지 않으면 위 재생 버튼을 눌러주세요.")
    except Exception:
        st.warning("음성을 만들지 못했습니다. 화면의 글자를 확인해주세요.")


def build_message(number, target):
    """인식 결과와 기다리는 버스를 비교해 안내 문장을 만든다."""
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
# 화면 구성
# ---------------------------------------------------------
st.markdown('<div class="title-box">🚌 버스 번호 인식</div>', unsafe_allow_html=True)

api_key = get_api_key()
if not api_key:
    st.error("GEMINI_API_KEY가 설정되지 않았습니다. 배포 설정의 Secrets에 키를 넣어주세요.")
    st.stop()

try:
    client = get_client(api_key)
except Exception:
    st.error("AI를 준비하지 못했습니다. API 키를 확인해주세요.")
    st.stop()

# 기다리는 버스 번호 (선택)
target_bus = st.text_input(
    "기다리는 버스 번호 (선택)",
    placeholder="예: 14",
    help="입력하면 도착한 버스가 맞는지 함께 알려드립니다.",
).strip()

st.markdown('<div class="guide-text">📷 버스를 비춰주세요</div>', unsafe_allow_html=True)

photo = st.camera_input(
    "카메라 촬영",
    key=f"camera_{st.session_state.camera_key}",
    label_visibility="collapsed",
)

# 카메라가 안 될 때를 위한 사진 업로드
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

        # 같은 사진은 다시 분석하지 않음
        if image_hash != st.session_state.last_hash:
            with st.spinner("버스 번호를 읽고 있습니다..."):
                try:
                    number = recognize_bus_number(client, image_bytes, mime_type)
                    if number:
                        st.session_state.result = {
                            "ok": True,
                            "message": build_message(number, target_bus),
                        }
                    else:
                        st.session_state.result = {"ok": False, "message": FAIL_MESSAGE}
                except Exception as e:
                    st.session_state.result = {"ok": False, "message": error_message(e)}
            st.session_state.last_hash = image_hash
    except Exception:
        st.session_state.result = {"ok": False, "message": "사진을 읽지 못했습니다. 다시 촬영해주세요."}

# ---------------------------------------------------------
# 결과 표시 + 음성 안내
# ---------------------------------------------------------
result = st.session_state.result
if result:
    if result["ok"]:
        st.markdown(f'<div class="result-box">🔊 {result["message"]}</div>', unsafe_allow_html=True)
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

st.markdown("---")
st.caption("※ AI 인식은 틀릴 수 있습니다. 탑승 전 기사님께 한 번 더 확인하세요.")
