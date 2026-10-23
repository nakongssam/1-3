
import streamlit as st
from collections import deque

st.set_page_config(
    page_title="쉬운 지하철 길찾기",
    page_icon="🚇",
    layout="centered"
)

# 화면 디자인
st.markdown("""
<style>
.stApp {
    background-color: #D2E4F4;
}
.block-container {
    max-width: 750px;
    padding-top: 30px;
}
h1 {
    text-align: center;
    color: #172B4D;
}
.stSelectbox label {
    font-size: 24px !important;
    font-weight: bold;
}
div[data-baseweb="select"] {
    font-size: 22px;
}
.stButton > button {
    background-color: #F02020;
    color: white;
    font-size: 26px;
    font-weight: bold;
    width: 100%;
    min-height: 65px;
    border-radius: 12px;
    border: none;
}
.stButton > button:hover {
    background-color: #C90000;
    color: white;
}
.result {
    background-color: white;
    padding: 22px;
    border-radius: 15px;
    font-size: 22px;
    line-height: 1.9;
    color: #172B4D;
}
</style>
""", unsafe_allow_html=True)

# 서울 지하철 일부 주요 역
lines = {
    "1호선": [
        "서울역", "시청", "종각", "종로3가",
        "종로5가", "동대문", "동묘앞", "신설동"
    ],
    "2호선": [
        "시청", "을지로입구", "을지로3가",
        "을지로4가", "동대문역사문화공원",
        "신당", "왕십리", "성수", "건대입구",
        "잠실", "종합운동장", "삼성", "선릉",
        "역삼", "강남", "교대", "사당",
        "신도림", "홍대입구", "신촌",
        "이대", "아현", "충정로"
    ],
    "3호선": [
        "구파발", "연신내", "불광", "녹번",
        "홍제", "독립문", "경복궁", "안국",
        "종로3가", "을지로3가", "충무로",
        "동대입구", "약수", "금호", "옥수",
        "신사", "고속터미널", "교대",
        "남부터미널", "양재", "도곡",
        "대치", "학여울", "대청", "수서"
    ],
    "4호선": [
        "혜화", "동대문", "동대문역사문화공원",
        "충무로", "명동", "회현", "서울역",
        "숙대입구", "삼각지", "신용산",
        "이촌", "동작", "총신대입구(이수)",
        "사당"
    ],
    "5호선": [
        "김포공항", "마곡", "발산", "까치산",
        "목동", "오목교", "영등포구청",
        "신길", "여의도", "마포", "공덕",
        "충정로", "서대문", "광화문",
        "종로3가", "을지로4가",
        "동대문역사문화공원", "청구",
        "왕십리", "군자", "천호"
    ],
    "6호선": [
        "응암", "역촌", "불광", "독바위",
        "연신내", "디지털미디어시티",
        "월드컵경기장", "합정", "상수",
        "광흥창", "대흥", "공덕",
        "효창공원앞", "삼각지", "이태원",
        "약수", "청구", "신당", "동묘앞",
        "안암", "석계"
    ],
    "7호선": [
        "장암", "도봉산", "노원", "태릉입구",
        "먹골", "중화", "상봉", "면목",
        "군자", "어린이대공원", "건대입구",
        "강남구청", "논현", "반포",
        "고속터미널", "내방",
        "총신대입구(이수)", "남성",
        "숭실대입구", "보라매", "신풍",
        "대림", "가산디지털단지",
        "철산", "광명사거리", "온수"
    ],
    "8호선": [
        "별내", "다산", "구리", "암사역사공원",
        "암사", "천호", "강동구청", "몽촌토성",
        "잠실", "석촌", "송파", "가락시장",
        "문정", "장지", "복정", "산성",
        "남한산성입구", "단대오거리", "신흥",
        "수진", "모란"
    ],
    "9호선": [
        "개화", "김포공항", "가양", "염창",
        "당산", "국회의사당", "여의도",
        "노량진", "동작", "고속터미널",
        "신논현", "언주", "선정릉",
        "봉은사", "종합운동장", "석촌",
        "올림픽공원", "중앙보훈병원"
    ]
}

# 노선별 색상
colors = {
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

# 역과 호선을 함께 관리하는 그래프
graph = {}

def connect(a, b, cost):
    graph.setdefault(a, []).append((b, cost))
    graph.setdefault(b, []).append((a, cost))

station_lines = {}

for line, stations in lines.items():
    for station in stations:
        station_lines.setdefault(station, []).append(line)

    for i in range(len(stations) - 1):
        a = (stations[i], line)
        b = (stations[i + 1], line)
        connect(a, b, 0)

# 같은 역에서 다른 호선으로 환승
for station, available in station_lines.items():
    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            connect(
                (station, available[i]),
                (station, available[j]),
                1
            )

# 0-1 BFS: 환승 횟수 최소화
def find_route(start, end):
    if start == end:
        return [], 0

    queue = deque()
    distance = {}
    previous = {}

    for line in station_lines[start]:
        node = (start, line)
        distance[node] = 0
        previous[node] = None
        queue.append(node)

    while queue:
        current = queue.popleft()

        for next_node, cost in graph.get(current, []):
            new_dist = distance[current] + cost

            if new_dist < distance.get(next_node, float("inf")):
                distance[next_node] = new_dist
                previous[next_node] = current

                if cost == 0:
                    queue.appendleft(next_node)
                else:
                    queue.append(next_node)

    ends = [
        (end, line)
        for line in station_lines[end]
        if (end, line) in distance
    ]

    if not ends:
        return [], 0

    target = min(ends, key=lambda x: distance[x])
    transfers = distance[target]

    path = []
    while target is not None:
        path.append(target)
        target = previous[target]

    path.reverse()
    return path, transfers


# 화면
st.title("🚇 쉬운 지하철 길찾기")

st.markdown(
    "<h3 style='text-align:center;'>"
    "어디로 가시나요?</h3>",
    unsafe_allow_html=True
)

stations = sorted(station_lines.keys())

col1, col2 = st.columns(2)

with col1:
    start = st.selectbox(
        "🚉 출발역",
        stations,
        index=stations.index("서울역")
    )

with col2:
    end = st.selectbox(
        "🏁 도착역",
        stations,
        index=stations.index("시청")
    )

st.write("")

if st.button("🔍 길찾기", type="primary"):

    if start == end:
        st.warning("출발역과 도착역이 같습니다.")

    else:
        try:
            path, transfers = find_route(start, end)

            if not path:
                st.error("경로를 찾을 수 없습니다.")

            else:
                st.success("길을 찾았습니다!")

                st.markdown(
                    f"<div class='result'>"
                    f"<b>🚉 출발:</b> {start}<br>"
                    f"<b>🏁 도착:</b> {end}<br>"
                    f"<b>🔄 환승:</b> {transfers}번"
                    f"</div>",
                    unsafe_allow_html=True
                )

                # 이동 안내 단계 생성
                steps = []
                current_line = path[0][1]
                section_start = path[0][0]

                for i in range(1, len(path)):
                    station, line = path[i]

                    if line != current_line:
                        steps.append(
                            (current_line, section_start, station)
                        )
                        current_line = line
                        section_start = station

                steps.append(
                    (current_line, section_start, end)
                )

                st.subheader("📍 이렇게 이동하세요")

                for i, (line, a, b) in enumerate(steps):
                    color = colors.get(line, "#444444")

                    st.markdown(
                        f"<div style='background:white;"
                        f"padding:18px;border-radius:12px;"
                        f"margin-bottom:12px;"
                        f"border-left:9px solid {color};"
                        f"color:#172B4D;font-size:22px;'>"
                        f"<b>{i+1}. {line} 탑승</b><br>"
                        f"{a} → {b}"
                        f"</div>",
                        unsafe_allow_html=True
                    )

                    if i < len(steps) - 1:
                        st.info(f"🔄 {b}역에서 환승하세요.")

                if transfers == 0:
                    st.success(
                        "😊 환승 없이 이동할 수 있습니다!"
                    )

        except Exception:
            st.error(
                "길찾기 중 문제가 발생했습니다. "
                "다시 시도해 주세요."
            )

st.divider()

st.caption(
    "⚠️ 이 앱은 학습용 예시입니다. "
    "서울 지하철 일부 역만 포함하며, "
    "실제 최단 경로·소요 시간·운행 정보를 "
    "보장하지 않습니다. "
    "일부 노선의 역이 생략되어 있으며 "
    "실제 연결 관계와 다를 수 있습니다."
)
