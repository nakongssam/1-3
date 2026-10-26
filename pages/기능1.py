import streamlit as st
from urllib.parse import quote
import re
import json
from html import escape
import streamlit.components.v1 as components

st.set_page_config(page_title='안심지하철 | 보호자 연락 시스템', page_icon='🚇', layout='centered')

st.markdown('''<style>
.stApp {background:linear-gradient(180deg,#edf5ff 0%,#ffffff 55%);}
.block-container {max-width:720px;padding-top:1.5rem;}
h1,h2,h3 {color:#184b92!important;}
.stButton>button {width:100%;border-radius:16px;min-height:58px;font-size:21px;font-weight:700;background:#3178ed;color:white;border:0;}
.stButton>button:hover {background:#195bc2;color:white;}
[data-testid="stTextInput"] input {font-size:20px;border-radius:12px;}
.hero {padding:23px;border-radius:22px;background:linear-gradient(125deg,#276fe1,#68a3fa);color:white;margin-bottom:18px;}
.hero h1 {color:white!important;margin:0;font-size:31px;}
.hero p {margin:7px 0 0;font-size:17px;}
.panel {padding:20px;background:#eaf3ff;border-radius:18px;margin:12px 0;color:#174780;}
.status {text-align:center;padding:24px;background:#e9f9f2;border-radius:20px;font-size:23px;color:#087c64;font-weight:700;}
</style>''', unsafe_allow_html=True)

if 'stage' not in st.session_state:
    st.session_state.stage = '출발 전'
if 'route' not in st.session_state:
    st.session_state.route = ('', '')

st.markdown('<div class="hero"><h1>🚇 안심지하철</h1><p>어르신의 안전한 이동을 돕는 보호자 연락 시스템</p></div>', unsafe_allow_html=True)
st.info('📍 실제 위치를 자동으로 확인하지 않습니다. 도착 여부는 이용자가 직접 확인합니다.')

st.subheader('① 이동 경로 입력')
start = st.text_input('🚉 출발역', placeholder='예: 천안역')
end = st.text_input('🏁 도착역', placeholder='예: 서울역')

st.subheader('② 보호자 정보')
guardian = st.text_input('👨‍👩‍👧 보호자 이름', placeholder='예: 김보호')
phone = st.text_input('📱 보호자 휴대전화 번호', placeholder='예: 01012345678')
clean_phone = re.sub(r'[^0-9]', '', phone)
valid_phone = bool(re.fullmatch(r'01[016789]\d{7,8}', clean_phone))

if (start.strip(), end.strip()) != st.session_state.route:
    st.session_state.route = (start.strip(), end.strip())
    st.session_state.stage = '출발 전'

st.markdown(f'<div class="panel"><b>🚉 {escape(start.strip()) or "출발역"} &nbsp; → &nbsp; {escape(end.strip()) or "도착역"}</b><br>현재 상태: {st.session_state.stage}</div>', unsafe_allow_html=True)

st.subheader('③ 이동 상태')
if st.session_state.stage == '출발 전':
    if st.button('🚇 출발했어요'):
        if not start.strip() or not end.strip():
            st.warning('출발역과 도착역을 먼저 입력해주세요.')
        elif start.strip() == end.strip():
            st.warning('출발역과 도착역을 다르게 입력해주세요.')
        else:
            st.session_state.stage = '이동 중'
            st.rerun()
elif st.session_state.stage == '이동 중':
    st.info('🚆 이동 중입니다. 도착역에 내린 뒤 아래 버튼을 눌러주세요.')
    if st.button('✅ 목적지에 도착했어요'):
        st.session_state.stage = '도착 완료'
        st.rerun()
else:
    st.markdown('<div class="status">✅ 목적지에 도착했어요!</div>', unsafe_allow_html=True)
    if st.button('🔄 새로운 이동 시작'):
        st.session_state.stage = '출발 전'
        st.rerun()

st.subheader('④ 보호자에게 도착 알리기')
if st.session_state.stage == '도착 완료':
    if not guardian.strip() or not valid_phone:
        st.warning('보호자 이름과 올바른 휴대전화 번호를 입력해주세요.')
    else:
        message = f'[안심지하철] {guardian.strip()}님, 이용자가 {end.strip()}에 도착했다고 직접 확인했습니다. 출발역: {start.strip()}. 안심하세요!'
        st.text_area('보호자에게 보낼 메시지', value=message, height=110)
        st.code(clean_phone, language=None)
        st.caption('아래 링크를 휴대전화에서 누르면 문자 앱이 열립니다. 전송 버튼은 직접 눌러야 합니다.')
        sms_url = 'sms:' + clean_phone + '?body=' + quote(message)
        st.markdown(f'<a href="{sms_url}" target="_self" style="display:block;text-align:center;background:#3178ed;color:white;padding:18px;border-radius:16px;font-size:21px;font-weight:bold;text-decoration:none;">📩 문자 앱 열기</a>', unsafe_allow_html=True)
        st.code(message, language=None)
        st.caption('문자 앱이 열리지 않는 PC에서는 위 메시지를 복사해 휴대전화로 보내주세요.')
else:
    st.info('도착 완료 버튼을 누르면 보호자에게 보낼 문자 내용이 나타납니다.')

st.subheader('🔊 음성 안내')
voice_text = f'안심지하철입니다. 현재 상태는 {st.session_state.stage}입니다. 출발역은 {start or "미입력"}, 도착역은 {end or "미입력"}입니다.'
# Browser speech synthesis: no extra package, browser support required.
components.html('''<button onclick="speak()" style="width:100%;padding:16px;background:#e6f1ff;color:#174b95;border:1px solid #a9cbfa;border-radius:14px;font-size:20px;font-weight:bold;cursor:pointer">🔊 안내 듣기</button>
<script>function speak(){if(!('speechSynthesis' in window)){alert('이 브라우저는 음성 안내를 지원하지 않습니다.');return;}window.speechSynthesis.cancel();let u=new SpeechSynthesisUtterance(TEXT);u.lang='ko-KR';u.rate=0.85;window.speechSynthesis.speak(u);}</script>'''.replace('TEXT', json.dumps(voice_text, ensure_ascii=False)), height=70)

st.caption('🔒 입력 정보는 현재 앱 세션에서만 사용합니다. 이 앱은 위치 추적이나 자동 문자 발송을 제공하지 않습니다.')
