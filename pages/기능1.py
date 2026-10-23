
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="소리로만 하는 축구",
    page_icon="⚽",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(145deg, #f8fcff, #dcecff);
}
.block-container {
    max-width: 720px;
    padding: 1rem 0.5rem 2rem;
}
header[data-testid="stHeader"] {
    background: transparent;
}
#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
* {box-sizing:border-box}
body {
    margin:0;
    font-family:Arial,'Malgun Gothic',sans-serif;
    color:#245078;
    background:transparent;
}
.app {
    max-width:550px;
    margin:auto;
    background:#f5faff;
    border-radius:30px;
    overflow:hidden;
    box-shadow:0 15px 40px #80a6d044;
}
.hero {
    background:linear-gradient(135deg,#72a8ff,#a5d9ff 65%,#d4f6ff);
    padding:27px 24px 32px;
    color:white;
    position:relative;
}
.brand {
    font-size:14px;
    font-weight:bold;
    letter-spacing:2px;
    opacity:.95;
}
.hero h1 {
    margin:20px 0 8px;
    font-size:32px;
    line-height:1.25;
}
.hero p {
    font-size:15px;
    line-height:1.6;
    margin:0;
}
.hero-ball {
    position:absolute;
    right:25px;
    top:65px;
    font-size:60px;
    opacity:.85;
}
.content {padding:20px}
.stats {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:8px;
    margin-bottom:17px;
}
.stat {
    background:white;
    border-radius:16px;
    padding:13px 3px;
    text-align:center;
    box-shadow:0 4px 12px #a6c8e72b;
}
.stat small {
    display:block;
    font-size:12px;
    color:#7499bc;
}
.stat strong {
    display:block;
    font-size:24px;
    color:#347cda;
    margin-top:4px;
}
.game-card {
    background:white;
    padding:12px;
    border-radius:22px;
    box-shadow:0 5px 18px #8db5d02a;
}
.field {
    height:260px;
    position:relative;
    overflow:hidden;
    border-radius:16px;
    background:linear-gradient(180deg,#b8e7ff,#7ebfe9);
}
.goal {
    position:absolute;
    left:23%;
    top:20px;
    width:54%;
    height:95px;
    border:6px solid white;
    border-radius:7px 7px 0 0;
    background:
      repeating-linear-gradient(90deg,transparent 0 19px,#ffffff70 20px 22px),
      repeating-linear-gradient(0deg,transparent 0 19px,#ffffff70 20px 22px);
    box-shadow:0 4px 12px #458ac255;
}
.ground {
    position:absolute;
    bottom:-40px;
    width:130%;
    left:-15%;
    height:125px;
    border-radius:50%;
    background:#8ed3b2;
}
.keeper {
    position:absolute;
    bottom:18px;
    left:50%;
    transform:translateX(-50%);
    font-size:63px;
}
.ball {
    position:absolute;
    top:130px;
    left:50%;
    transform:translateX(-50%);
    font-size:44px;
    transition:left .3s,top .3s;
}
.message {
    margin-top:12px;
    background:#eaf5ff;
    border-radius:13px;
    padding:16px 10px;
    min-height:68px;
    text-align:center;
    font-size:19px;
    font-weight:bold;
    color:#286cae;
}
.section-title {
    font-size:17px;
    font-weight:bold;
    margin:22px 2px 12px;
}
.buttons {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:10px;
}
button {
    border:0;
    border-radius:15px;
    min-height:67px;
    padding:12px 8px;
    font-size:17px;
    font-weight:bold;
    cursor:pointer;
    touch-action:manipulation;
}
button:focus-visible {
    outline:4px solid #ffad32;
    outline-offset:3px;
}
.primary {
    background:linear-gradient(135deg,#498ef5,#77b8ff);
    color:white;
    box-shadow:0 5px 12px #579de555;
}
.catch {
    background:#fff1b9;
    color:#765313;
}
.secondary {
    background:white;
    color:#397db9;
    border:2px solid #d8eafb;
}
button:disabled {opacity:.5;cursor:not-allowed}
.guide {
    margin-top:22px;
    padding:19px;
    background:white;
    border-radius:18px;
    font-size:15px;
    line-height:1.9;
    color:#537a9c;
}
.guide b {color:#276ba8}
.footer {
    text-align:center;
    padding:18px 8px 25px;
    font-size:12px;
    color:#8daac4;
}
@media(max-width:420px) {
    .hero h1 {font-size:27px}
    .hero-ball {font-size:42px;top:82px}
    .content {padding:13px}
    .field {height:230px}
    .stat strong {font-size:21px}
    button {font-size:15px}
}
</style>
</head>
<body>
<div class="app">
  <div class="hero">
    <div class="brand">⚽ SOUND FOOTBALL</div>
    <h1>소리로만 하는<br>축구 게임</h1>
    <p>눈이 아닌 귀로 느끼는 축구!<br>
       소리를 듣고 공을 막아보세요.</p>
    <div class="hero-ball" aria-hidden="true">⚽</div>
  </div>

  <div class="content">
    <div class="stats">
      <div class="stat"><small>점수</small><strong id="score">0</strong></div>
      <div class="stat"><small>최고점수</small><strong id="best">0</strong></div>
      <div class="stat"><small>기회</small><strong id="lives">5</strong></div>
      <div class="stat"><small>레벨</small><strong id="level">1</strong></div>
    </div>

    <div class="game-card">
      <div class="field" aria-hidden="true">
        <div class="goal"></div>
        <div class="ground"></div>
        <div class="ball" id="ball">⚽</div>
        <div class="keeper">🧤</div>
      </div>
      <div class="message" id="message" role="status" aria-live="polite">
        🎧 게임 시작을 눌러주세요!
      </div>
    </div>

    <div class="section-title">🎮 게임 조작</div>
    <div class="buttons">
      <button class="primary" id="start" onclick="startGame()">
        ▶ 게임 시작
      </button>
      <button class="catch" id="catch" onclick="catchBall()" disabled>
        🧤 공 막기!
      </button>
      <button class="secondary" id="sound" onclick="toggleSound()">
        🔊 음성 켜짐
      </button>
      <button class="secondary" onclick="resetGame()">
        ↻ 다시 시작
      </button>
    </div>

    <div class="guide">
      <b>💙 게임 이용 방법</b><br>
      ① 게임 시작 버튼을 누르세요.<br>
      ② 공이 오는 방향을 소리로 들어보세요.<br>
      ③ 3, 2, 1 카운트다운을 기다리세요.<br>
      ④ "지금!" 소리가 나면 공 막기를 누르세요.<br>
      ⑤ 성공하면 10점을 얻고 난이도가 올라갑니다.<br>
      ⌨️ 키보드 스페이스바로도 막을 수 있어요.
    </div>
  </div>
  <div class="footer">SOUND FOOTBALL · 김소민</div>
</div>

<script>
let score=0,best=0,lives=5,level=1;
let running=false,active=false,soundOn=true;
let timers=[],roundId=0,targetTime=0;

const el=id=>document.getElementById(id);

function later(fn,ms) {
    const t=setTimeout(fn,ms);
    timers.push(t);
}
function clearAll() {
    timers.forEach(clearTimeout);
    timers=[];
}
function say(text) {
    if(!soundOn || !('speechSynthesis' in window)) return;
    try {
        speechSynthesis.cancel();
        const u=new SpeechSynthesisUtterance(text);
        u.lang="ko-KR";
        u.rate=1.05;
        speechSynthesis.speak(u);
    } catch(e) {console.log(e)}
}
function show(text) {el("message").textContent=text}
function update() {
    el("score").textContent=score;
    el("best").textContent=best;
    el("lives").textContent=lives;
    el("level").textContent=level;
}
function resetGame() {
    roundId++;
    clearAll();
    if('speechSynthesis' in window) speechSynthesis.cancel();
    score=0;lives=5;level=1;
    running=false;active=false;
    el("catch").disabled=true;
    el("start").disabled=false;
    el("ball").style.left="50%";
    el("ball").style.top="130px";
    show("🎧 게임 시작을 눌러주세요!");
    update();
}
function toggleSound() {
    soundOn=!soundOn;
    el("sound").textContent=soundOn?"🔊 음성 켜짐":"🔇 음성 꺼짐";
    if(soundOn) say("음성이 켜졌습니다.");
    else if('speechSynthesis' in window) speechSynthesis.cancel();
}
function startGame() {
    if(running)return;
    resetGame();
    running=true;
    el("start").disabled=true;
    show("⚽ 게임이 시작됩니다!");
    say("게임 시작! 소리에 집중하세요.");
    later(nextRound,1800);
}
function nextRound() {
    if(!running)return;
    roundId++;
    clearAll();
    active=false;
    el("catch").disabled=true;
    const id=roundId;
    const dirs=["왼쪽","가운데","오른쪽"];
    const direction=dirs[Math.floor(Math.random()*3)];
    const pos={"왼쪽":"25%","가운데":"50%","오른쪽":"75%"};
    el("ball").style.left=pos[direction];
    el("ball").style.top="130px";

    show("🔊 "+direction+"에서 공이 옵니다!");
    say(direction+"에서 공이 옵니다.");

    const interval=Math.max(550,1100-(level-1)*100);
    const delay=1500;

    for(let n=3;n>=1;n--) {
        later(()=>{
            if(id!==roundId||!running)return;
            show("⚽ "+direction+" · "+n);
            say(String(n));
        },delay+(3-n)*interval);
    }

    const hit=delay+3*interval;
    const windowMs=Math.max(350,750-(level-1)*50);

    later(()=>{
        if(id!==roundId||!running)return;
        targetTime=performance.now();
        active=true;
        el("catch").disabled=false;
        el("ball").style.top="175px";
        show("🧤 지금! 공을 막으세요!");
        say("지금!");
    },hit);

    later(()=>{
        if(id!==roundId||!running||!active)return;
        active=false;
        el("catch").disabled=true;
        miss("시간 초과! 골을 허용했어요.");
    },hit+windowMs);
}
function catchBall() {
    if(!running||!active)return;
    active=false;
    el("catch").disabled=true;
    clearAll();

    const windowMs=Math.max(350,750-(level-1)*50);
    if(performance.now()-targetTime<=windowMs) {
        score+=10;
        best=Math.max(best,score);
        level=Math.min(8,Math.floor(score/30)+1);
        show("🎉 멋진 선방! +10점");
        say("성공! 멋진 선방입니다.");
        update();
        later(nextRound,1800);
    } else {
        miss("아쉬워요! 공을 놓쳤어요.");
    }
}
function miss(text) {
    lives--;
    show("🥅 "+text);
    say(text);
    update();
    if(lives<=0) {
        running=false;
        active=false;
        el("catch").disabled=true;
        el("start").disabled=false;
        show("🏁 게임 종료! 최종 점수 "+score+"점");
        say("게임 종료. 최종 점수 "+score+"점.");
    } else {
        later(nextRound,1800);
    }
}
document.addEventListener("keydown",e=>{
    if(e.code==="Space") {
        e.preventDefault();
        if(active)catchBall();
    }
});
update();
</script>
</body>
</html>
"""

components.html(html, height=1050, scrolling=True)
