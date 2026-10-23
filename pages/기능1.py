
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="소리로만 하는 축구",
    page_icon="⚽",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f0f7ff;
}
.block-container {
    max-width: 1050px;
    padding-top: 1.5rem;
}
h1 {
    text-align: center;
    color: #164b79;
}
</style>
""", unsafe_allow_html=True)

st.title("⚽ 소리로만 하는 축구")
st.markdown(
    "<p style='text-align:center;font-size:20px;'>"
    "소리를 듣고 공을 막아보세요!</p>",
    unsafe_allow_html=True
)

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f0f7ff;
    color: #183b57;
}
.container {
    max-width: 850px;
    margin: auto;
    padding: 12px;
}
.scoreboard {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 15px;
}
.score {
    background: white;
    border-radius: 14px;
    padding: 12px;
    min-width: 105px;
    text-align: center;
    font-weight: bold;
    font-size: 18px;
    border: 2px solid #c9dff2;
}
.score strong {
    display: block;
    font-size: 27px;
    color: #1263aa;
}
.field {
    position: relative;
    height: 300px;
    overflow: hidden;
    background: linear-gradient(
        #74bf7c, #3e9959
    );
    border: 5px solid white;
    border-radius: 18px;
}
.field::after {
    content: "";
    position: absolute;
    inset: 20px;
    border: 2px solid rgba(255,255,255,.5);
    border-radius: 8px;
    pointer-events: none;
}
.goal {
    position: absolute;
    top: 10px;
    left: 25%;
    width: 50%;
    height: 85px;
    border: 6px solid white;
    background:
      repeating-linear-gradient(
        0deg, transparent 0 16px,
        #ffffff55 17px 19px
      ),
      repeating-linear-gradient(
        90deg, transparent 0 20px,
        #ffffff55 21px 23px
      );
}
.player {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 65px;
}
.ball {
    position: absolute;
    top: 105px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 48px;
    transition: left .3s;
}
.message {
    background: white;
    border: 3px solid #b7d8f3;
    border-radius: 14px;
    padding: 18px;
    margin: 15px 0;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    min-height: 75px;
}
.controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}
button {
    border: none;
    border-radius: 15px;
    padding: 20px 10px;
    font-size: 21px;
    font-weight: bold;
    cursor: pointer;
    touch-action: manipulation;
}
button:focus-visible {
    outline: 4px solid #ffae00;
    outline-offset: 3px;
}
.start { background: #1675c5; color: white; }
.catch { background: #ffcf4a; color: #222; }
.sound { background: #e3eaf1; color: #183b57; }
.reset { background: #e8dff5; color: #402d66; }
button:disabled {
    opacity: .5;
    cursor: not-allowed;
}
.help {
    background: white;
    border-radius: 14px;
    padding: 15px;
    margin-top: 15px;
    font-size: 17px;
    line-height: 1.7;
}
@media(max-width: 500px) {
    .field { height: 240px; }
    button { font-size: 18px; }
    .message { font-size: 20px; }
}
</style>
</head>
<body>
<div class="container">

<div class="scoreboard">
  <div class="score">점수<strong id="score">0</strong></div>
  <div class="score">최고 점수<strong id="best">0</strong></div>
  <div class="score">기회<strong id="lives">5</strong></div>
  <div class="score">레벨<strong id="level">1</strong></div>
</div>

<div class="field" aria-hidden="true">
  <div class="goal"></div>
  <div class="ball" id="ball">⚽</div>
  <div class="player">🧤</div>
</div>

<div class="message" id="message"
     role="status" aria-live="polite">
  시작 버튼을 눌러주세요!
</div>

<div class="controls">
  <button class="start" id="start"
    onclick="startGame()">▶ 게임 시작</button>
  <button class="catch" id="catch"
    onclick="catchBall()" disabled>
    🧤 공 막기!
  </button>
  <button class="sound" id="sound"
    onclick="toggleSound()">
    🔊 음성 켜짐
  </button>
  <button class="reset"
    onclick="resetGame()">🔄 다시 시작</button>
</div>

<div class="help">
  <b>🎧 게임 방법</b><br>
  ① 게임 시작을 누릅니다.<br>
  ② 왼쪽, 가운데, 오른쪽 음성 안내를 듣습니다.<br>
  ③ 숫자 카운트다운에 집중합니다.<br>
  ④ "지금!" 소리에 맞춰 공 막기 버튼을 누릅니다.<br>
  ⑤ 성공할수록 공이 더 빠르게 날아옵니다.<br>
  ⌨️ 스페이스바로도 공을 막을 수 있습니다.<br>
  ※ 이어폰 사용을 권장합니다.
</div>

</div>

<script>
let score = 0;
let best = 0;
let lives = 5;
let level = 1;
let running = false;
let soundOn = true;
let direction = "";
let targetTime = 0;
let active = false;
let timers = [];
let roundId = 0;

const msg = document.getElementById("message");
const ball = document.getElementById("ball");
const catchButton = document.getElementById("catch");
const startButton = document.getElementById("start");

function schedule(fn, delay) {
    const id = setTimeout(fn, delay);
    timers.push(id);
}
function clearTimers() {
    timers.forEach(clearTimeout);
    timers = [];
}
function speak(text) {
    if (!soundOn) return;
    if (!("speechSynthesis" in window)) return;
    try {
        window.speechSynthesis.cancel();
        const voice = new SpeechSynthesisUtterance(text);
        voice.lang = "ko-KR";
        voice.rate = 1.05;
        window.speechSynthesis.speak(voice);
    } catch (e) {
        console.log("음성 출력 실패", e);
    }
}
function update() {
    document.getElementById("score").textContent = score;
    document.getElementById("best").textContent = best;
    document.getElementById("lives").textContent = lives;
    document.getElementById("level").textContent = level;
}
function show(text) {
    msg.textContent = text;
}
function toggleSound() {
    soundOn = !soundOn;
    document.getElementById("sound").textContent =
        soundOn ? "🔊 음성 켜짐" : "🔇 음성 꺼짐";
    if (soundOn) speak("음성이 켜졌습니다.");
    else if ("speechSynthesis" in window)
        window.speechSynthesis.cancel();
}
function resetGame() {
    roundId++;
    clearTimers();
    if ("speechSynthesis" in window)
        window.speechSynthesis.cancel();
    running = false;
    active = false;
    score = 0;
    lives = 5;
    level = 1;
    targetTime = 0;
    ball.style.left = "50%";
    catchButton.disabled = true;
    startButton.disabled = false;
    show("시작 버튼을 눌러주세요!");
    update();
}
function startGame() {
    if (running) return;
    resetGame();
    running = true;
    startButton.disabled = true;
    show("게임이 시작됩니다!");
    speak("게임 시작! 소리에 집중하세요.");
    schedule(nextRound, 1800);
}
function nextRound() {
    if (!running) return;
    roundId++;
    clearTimers();
    active = false;
    catchButton.disabled = true;

    const current = roundId;
    const dirs = ["왼쪽", "가운데", "오른쪽"];
    direction = dirs[Math.floor(Math.random() * 3)];

    const positions = {
        "왼쪽": "25%",
        "가운데": "50%",
        "오른쪽": "75%"
    };
    ball.style.left = positions[direction];

    show(direction + "에서 공이 옵니다!");
    speak(direction + "에서 공이 옵니다.");

    // 레벨이 높아질수록 카운트다운이 빨라짐
    const interval = Math.max(550, 1100 - (level-1)*100);
    const startDelay = 1500;

    for (let n = 3; n >= 1; n--) {
        const delay = startDelay + (3-n)*interval;
        schedule(() => {
            if (current !== roundId || !running) return;
            show(direction + " · " + n);
            speak(String(n));
        }, delay);
    }

    const hitDelay = startDelay + 3*interval;

    schedule(() => {
        if (current !== roundId || !running) return;
        targetTime = performance.now();
        active = true;
        catchButton.disabled = false;
        show("⚽ 지금! 공을 막으세요!");
        speak("지금!");
    }, hitDelay);

    // 성공 가능 시간: 약 0.7초
    const windowMs = Math.max(350, 750-(level-1)*50);

    schedule(() => {
        if (current !== roundId || !running) return;
        if (active) {
            active = false;
            catchButton.disabled = true;
            missBall("시간 초과! 골을 허용했어요.");
        }
    }, hitDelay + windowMs);
}
function catchBall() {
    if (!running || !active) return;

    active = false;
    catchButton.disabled = true;
    clearTimers();

    const elapsed = performance.now() - targetTime;
    const windowMs = Math.max(350, 750-(level-1)*50);

    if (elapsed <= windowMs) {
        score += 10;
        best = Math.max(best, score);
        level = Math.min(8, Math.floor(score/30)+1);
        show("🎉 멋진 선방! +10점");
        speak("성공! 멋진 선방입니다.");
        update();
        schedule(nextRound, 1800);
    } else {
        missBall("아쉬워요! 공을 놓쳤어요.");
    }
}
function missBall(text) {
    lives--;
    show("🥅 " + text);
    speak(text);
    update();

    if (lives <= 0) {
        running = false;
        active = false;
        catchButton.disabled = true;
        startButton.disabled = false;
        show("🏁 게임 종료! 최종 점수: " + score + "점");
        speak("게임 종료. 최종 점수 " + score + "점.");
    } else {
        schedule(nextRound, 1800);
    }
}
document.addEventListener("keydown", (e) => {
    if (e.code === "Space") {
        e.preventDefault();
        if (active) catchBall();
    }
});
update();
</script>
</body>
</html>
"""

components.html(game_html, height=790, scrolling=True)

st.caption(
    "⚽ 시각장애인을 위한 소리 중심 축구 체험 게임 | "
    "김소민"
)
