import streamlit as st
from datetime import datetime
from urllib.parse import quote
import re

st.set_page_config(page_title='안심지하철 | 보호자 연락', page_icon='🚇', layout='centered', initial_sidebar_state='collapsed')

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp{font-family:'Noto Sans KR',sans-serif;}
.stApp{background:linear-gradient(155deg,#fff9fc 0%,#ffe5f0 58%,#ffd2e5 100%);}
.block-container{max-width:650px;padding-top:1.5rem;padding-bottom:4rem;}
#MainMenu,footer{visibility:hidden;}
h1,h2,h3,p{color:#49243b;}
.hero{background:linear-gradient(125deg,#f32192,#ff6b83);border-radius:28px;padding:28px 24px;color:white;box-shadow:0 12px 28px #ed438344;margin-bottom:22px;}
.hero h1{color:white;font-size:2.15rem;margin:8px 0;}.hero p{color:#fff6fb;margin:0;}
.pill{display:inline-block;border-radius:20px;padding:5px 12px;background:#ffffff30;font-size:13px;font-weight:700;color:white;}
.card{background:#ffffffd9;border:1px solid #fff;border-radius:24px;padding:20px;margin:10px 0 18px;box-shadow:0 7px 22px #ed43831a;}
.card h3{margin:0 0 8px;font-size:1.35rem;}.muted{color:#875a76;font-size:0.95rem;}
.route{font-size:1.35rem;font-weight:800;color:#c81c74;text-align:center;word-break:keep-all;}
.status{background:#fff1f7;border-radius:18px;padding:15px 18px;font-weight:700;color:#c51b71;margin:10px 0;}
div.stButton>button,div.stLinkButton>a{border-radius:30px!important;min-height:54px!important;font-size:1.05rem!important;font-weight:800!important;width:100%;}
div.stButton>button[kind="primary"]{background:linear-gradient(110deg,#f31b8c,#ff697e)!important;border:0!important;color:white!important;box-shadow:0 6px 16px #ef438644;}
div.stButton>button[kind="secondary"]{background:white!important;border:1px solid #f6a7c8!important;color:#be226e!important;}
input{border-radius:14px!important;} .stTextInput label{font-weight:700!important;}
[data-testid="stProgressBar"]>div>div{background:#f32192;}
.small{font-size:0.85rem;color:#885b75;}
</style>''', unsafe_allow_html=True)

for key, value in {'stage': 'setup', 'start': '', 'destination': '', 'guardian': '', 'phone': '', 'started_at': '', 'arrived_at': ''}.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown('''<div class="hero"><span class="pill">🚇 어르신을 위한 지하철 동행 서비스</span><h1>안심지하철 💗</h1><p>목적지까지 안심하고 이동하고,<br>보호자에게 도착 소식을 전해요.</p></div>''', unsafe_allow_html=True)

stage = st.session_state.stage
if stage == 'setup':
    st.markdown('<div class="card"><h3>📍 이동 계획 설정</h3><div class="muted">출발역과 도착역을 적어주세요.</div></div>', unsafe_allow_html=True)
    with st.form('setup_form'):
        start = st.text_input('🚉 출발역', value=st.session_state.start, placeholder='예: 천안역', max_chars=50)
        destination = st.text_input('🏁 도착역', value=st.session_state.destination, placeholder='예: 서울역', max_chars=50)
        st.markdown('### 👨‍👩‍👧 보호자 정보')
        guardian = st.text_input('보호자 이름', value=st.session_state.guardian, placeholder='예: 김보호', max_chars=40)
        phone = st.text_input('보호자 휴대전화 번호', value=st.session_state.phone, placeholder='예: 01012345678', max_chars=20)
        submitted = st.form_submit_button('이동 계획 확인 →', type='primary')
    if submitted:
        digits = re.sub(r'\D', '', phone)
        if not all([start.strip(), destination.strip(), guardian.strip(), digits]):
            st.error('출발역, 도착역, 보호자 이름과 전화번호를 모두 입력해주세요.')
        elif start.strip() == destination.strip():
            st.error('출발역과 도착역은 서로 달라야 합니다.')
        elif not re.fullmatch(r'01[016789]\d{7,8}', digits):
            st.error('보호자 휴대전화 번호를 확인해주세요. (예: 01012345678)')
        else:
            st.session_state.update(start=start.strip(), destination=destination.strip(), guardian=guardian.strip(), phone=digits, stage='confirm')
            st.rerun()

elif stage == 'confirm':
    st.markdown('<div class="card"><h3>💗 이동 계획을 확인해주세요</h3></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card"><div class="route">🚉 {st.session_state.start}　→　🏁 {st.session_state.destination}</div><p class="muted">보호자: {st.session_state.guardian}</p></div>', unsafe_allow_html=True)
    st.info('이동 중 상태는 이 화면에서 직접 확인합니다. 보호자에게 자동으로 위치가 전송되지는 않습니다.')
    if st.button('🚇 이동 시작하기', type='primary'):
        st.session_state.started_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        st.session_state.stage = 'moving'
        st.rerun()
    if st.button('← 정보 수정하기'):
        st.session_state.stage = 'setup'
        st.rerun()

elif stage == 'moving':
    st.markdown('<div class="card"><h3>🚇 지금 이동 중이에요</h3><div class="muted">목적지에 도착하면 아래 버튼을 눌러주세요.</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="card"><div class="status">📍 출발 완료 · {st.session_state.started_at}</div><div class="route">{st.session_state.start}<br>↓<br>🚇 이동 중<br>↓<br>{st.session_state.destination}</div><div class="status">🏁 도착 확인 대기 중</div></div>', unsafe_allow_html=True)
    st.warning('실시간 지하철 위치나 GPS를 확인하는 기능은 없습니다. 실제 도착했을 때만 버튼을 눌러주세요.')
    if st.button('✅ 목적지에 도착했어요!', type='primary'):
        st.session_state.arrived_at = datetime.now().strftime('%Y-%m-%d %H:%M')
        st.session_state.stage = 'arrived'
        st.rerun()
    if st.button('← 이동 계획으로 돌아가기'):
        st.session_state.stage = 'confirm'
        st.rerun()

elif stage == 'arrived':
    st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:4rem">🎉</div><h3>목적지에 도착했어요!</h3><div class="route">🏁 {st.session_state.destination}</div><p class="muted">{st.session_state.arrived_at}</p></div>', unsafe_allow_html=True)
    message = f'[{st.session_state.guardian}님께] 안녕하세요! {st.session_state.start}에서 출발해 {st.session_state.destination}에 안전하게 도착했습니다. 도착 확인 시간: {st.session_state.arrived_at} - 안심지하철'
    st.markdown('<div class="card"><h3>💌 보호자에게 알리기</h3><div class="muted">아래 메시지를 문자로 보낼 수 있어요.</div></div>', unsafe_allow_html=True)
    st.text_area('전송할 메시지', value=message, height=135)
    # Mobile SMS URI: opens the device messaging application; does not send automatically.
    sms_url = f'sms:{st.session_state.phone}?body={quote(message)}'
    st.link_button('📱 보호자에게 문자 작성하기', sms_url, type='primary')
    st.caption('휴대전화에서 문자 앱이 열리면 전송 버튼을 직접 눌러야 합니다. PC에서는 문자 앱이 열리지 않을 수 있습니다.')
    st.code(message, language=None)
    st.caption('문자 앱이 열리지 않으면 위 문구를 복사하여 직접 보내주세요.')
    if st.button('🏠 처음으로 돌아가기'):
        st.session_state.stage = 'setup'
        st.rerun()

st.markdown('<p class="small" style="text-align:center;margin-top:30px">💗 안심지하철 · 어르신의 안전한 이동을 응원합니다.</p>', unsafe_allow_html=True)
