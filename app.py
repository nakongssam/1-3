
import streamlit as st
from collections import deque

st.set_page_config(
    page_title="Easy Metro | 쉬운 지하철",
    page_icon="🚇",
    layout="centered"
)

# 디자인
st.markdown("""
<style>
.stApp {
    background: #F8FAF7;
}
.block-container {
    max-width: 680px;
    padding-top: 20px;
    padding-bottom: 50px;
}
h1, h2, h3 {
    color: #1B2B20 !important;
}
.hero {
    padding: 28px 5px 18px;
}
.hello {
    color: #62B76C;
    font-size: 20px;
    font-weight: 700;
}
.hero-title {
    color: #17291D;
    font-size: 38px;
    font-weight: 800;
    line-height: 1.35;
    margin: 12px 0;
}
.hero-desc {
    color: #728476;
    font-size: 17px;
}
.train-art {
    text-align: center;
    font-size: 95px;
    padding: 20px 0 35px;
    background:
        radial-gradient(circle at 35% 50%,
        #E1F5DF 0%, transparent 38%),
        radial-gradient(circle at 70% 45%,
        #FFF4C9 0%, transparent 30%);
    border-radius: 30px;
    margin-bottom: 20px;
}
.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #203B29;
    margin: 15px 0;
}
div[data-testid="stSelectbox"] label {
    font-size: 21px !important;
    font-weight: 700 !important;
    color: #23452E !important;
}
div[data-baseweb="select"] > div {
    background: #F0F7F0 !important;
    border: 1px solid #DCEBDD !important;
    border-radius: 15px !important;
    min-height: 60px;
    font-size: 21px;
}
.stButton > button {
    width: 100%;
    background: #287E4B !important;
    color: white !important;
    border: none !important;
    border-radius: 30px !important;
    min-height: 65px;
    font-size: 23px !important;
    font-weight: 800 !important;
}
.stButton > button:hover {
    background: #176238 !important;
    color: white !important;
}
.result-card {
    background: white;
    border: 1px solid #E0EDE1;
    border-radius: 20px;
    padding: 22px;
    margin: 16px 0;
    box-shadow: 0 5px 18px #193A2010;
    color: #203B29;
}
.result-title {
    color: #247B48;
    font-size: 23px;
    font-weight: 800;
}
.result-text {
    font-size: 20px;
    line-height: 2;
}
.route-step {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 16px;
    margin: 12px 0;
    font-size: 20px;
    color: #203B29;
}
.footer {
    text-align: center;
    color: #77947D;
    font-size: 15px;
    padding-top: 30px;
}
@media(max-width: 500px) {
    .hero-title {
        font-size: 31px;
    }
    .block-container {
        padding-left: 16px;
        padding-right: 16px;
    }
}
</style>
""", unsafe_allow_html=True)


# 일부 주요 역을 사용한 학습용 노선 데이터
# 실제 노선의 모든 역이 포함된 것은 아닙니다.
LINES = {
    "1호선": [
        "서울역", "시청", "종각", "종로3가",
        "종로5가", "동대문", "동묘앞", "신설동"
    ],
    "2호선": [
        "시청", "을지로입구", "을지로3가",
        "을지로4가", "동대문역사문화공원",
        "신당", "왕십리", "성수", "건대입구",
        "잠실", "종합운동장", "삼성",
        "선릉", "역삼", "강남", "교대",
        "사당"
    ],
    "3호선": [
        "경복궁", "안국", "종로3가",
        "을지로3가", "충무로", "약수",
        "신사", "고속터미널", "교대",
        "양재", "수서"
    ],
    "4호선": [
        "혜화", "동대문", "동대문역사문화공원",
        "충무로", "명동", "회현",
        "서울역", "삼각지", "사당"
    ],
    "5호선": [
        "김포공항", "여의도", "공덕",
        "충정로", "광화문", "종로3가",
        "을지로4가", "동대문역사문화공원",
        "왕십리", "군자", "천호"
    ],
    "6호선": [
        "불광", "연신내", "합정",
        "공덕", "삼각지", "약수",
        "신당", "동묘앞"
    ],
    "7호선": [
        "노원", "상봉", "군자",
        "건대입구", "강남구청",
        "고속터미널", "사당"
    ],
    "8호선": [
        "별내", "구리", "천호",
        "잠실", "석촌", "가락시장",
        "복정", "모란"
    ],
    "9호선": [
        "김포공항", "가양", "당산",
        "여의도", "노량진",
        "고속터미널", "신논현",
        "종합운동장", "석촌"
    ]
}

COLORS = {
    "1호선": "#0052A4",
    "2호선": "#00A84D",
    "3호선": "#EF7C1C",
    "4호선": "#00A5DE",
    "5호선": "#996CAC",
    "6호선": "#CD7C2F",
    "7호선": "#747F00",
    "8호선": "#E6186C",
    "9호선": "#BDB092"
}


# 역 연결 그래프 생성
graph = {}
station_lines = {}

def connect(a, b, cost):
    graph.setdefault(a, []).append((b, cost))
    graph.setdefault(b, []).append((a, cost))

for line, stations in LINES.items():
    for station in stations:
        station_lines.setdefault(station, []).append(line)

    for i in range(len(stations) - 1):
        connect(
            (stations[i], line),
            (stations[i + 1], line),
            0
        )

# 환승 연결
for station, available in station_lines.items():
    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            connect(
                (station, available[i]),
                (station, available[j]),
                1
            )


# 환승 횟수가 적은 경로 탐색
def find_route(start, end):
    queue = deque()
    dist = {}
    prev = {}

    for line in station_lines[start]:
        node = (start, line)
        queue.append(node)
        dist[node] = 0
        prev[node] = None

    while queue:
        current = queue.popleft()

        for next_node, cost in graph.get(current, []):
            new_cost = dist[current] + cost

            if new_cost < dist.get(next_node, float("inf")):
                dist[next_node] = new_cost
                prev[next_node] = current

                if cost == 0:
                    queue.appendleft(next_node)
                else:
                    queue.append(next_node)

    targets = [
        (end, line)
        for line in station_lines[end]
        if (end, line) in dist
    ]

    if not targets:
        return [], 0

    target = min(targets, key=lambda x: dist[x])
    transfers = dist[target]

    path = []
    while target is not None:
        path.append(target)
        target = prev[target]

    return path[::-1], transfers


# 상단
st.markdown("### ☰ &nbsp; EASY METRO 🌿")

st.markdown("""
<div class="hero">
    <div class="hello">Hello, Traveler! 👋</div>
    <div class="hero-title">
        오늘은 어디로<br>
        떠나시나요?
    </div>
    <div class="hero-desc">
        복잡한 지하철도 쉽고 편안하게.<br>
        목적지만 선택하면 길을 알려드려요.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="train-art">🚇 🌿</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">'
    '📍 나의 지하철 길찾기</div>',
    unsafe_allow_html=True
)

stations = sorted(station_lines.keys())

start = st.selectbox(
    "🟢 출발역",
    stations,
    index=stations.index("서울역")
)

st.markdown(
    "<h2 style='text-align:center;color:#28844C;'>"
    "↓</h2>",
    unsafe_allow_html=True
)

end = st.selectbox(
    "🔴 도착역",
    stations,
    index=stations.index("시청")
)

st.write("")

if st.button("🚇 길찾기 시작하기 →"):

    if start == end:
        st.warning(
            "출발역과 도착역이 같아요. "
            "다른 역을 선택해 주세요."
        )

    else:
        try:
            path, transfers = find_route(start, end)

            if not path:
                st.error(
                    "선택한 역 사이의 경로를 "
                    "찾지 못했어요."
                )

            else:
                st.markdown("""
                <div class="result-card">
                    <div class="result-title">
                        🌱 길을 찾았어요!
                    </div>
                    <p>아래 안내를 따라 이동해 보세요.</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(
                    f'<div class="result-card">'
                    f'<div class="result-text">'
                    f'🚉 <b>출발:</b> {start}<br>'
                    f'🏁 <b>도착:</b> {end}<br>'
                    f'🔄 <b>환승:</b> {transfers}번'
                    f'</div></div>',
                    unsafe_allow_html=True
                )

                # 탑승 구간 분리
                steps = []
                current_line = path[0][1]
                section_start = path[0][0]

                for station, line in path[1:]:
                    if line != current_line:
                        steps.append(
                            (current_line, section_start, station)
                        )
                        current_line = line
                        section_start = station

                steps.append(
                    (current_line, section_start, end)
                )

                st.subheader("🚉 이동 안내")

                for i, (line, a, b) in enumerate(steps):
                    color = COLORS.get(line, "#287E4B")

                    st.markdown(
                        f'<div class="route-step" '
                        f'style="border-left:8px solid {color};">'
                        f'<b>{i+1}. {line} 이용</b><br>'
                        f'{a} → {b}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    if i < len(steps) - 1:
                        st.info(
                            f"🔄 {b}역에서 "
                            f"{steps[i+1][0]}으로 환승하세요."
                        )

                if transfers == 0:
                    st.success(
                        "💚 환승 없이 갈 수 있어요!"
                    )

        except Exception:
            st.error(
                "일시적인 문제가 발생했어요. "
                "다시 시도해 주세요."
            )


st.markdown("""
<div class="footer">
    💚 누구나 쉽게 이용하는 지하철 안내<br>
    Made with Easy Metro
</div>
""", unsafe_allow_html=True)

st.caption(
    "⚠️ 학습용 시제품입니다. 일부 역만 포함하며 "
    "생략된 역 사이를 직접 연결한 단순화된 데이터이므로 "
    "실제 지하철 경로와 다를 수 있습니다. "
    "실제 이동 시 공식 지하철 길찾기를 확인하세요."
)
