import random
import time
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="생태계 크리처 시뮬레이터", page_icon="🐾", layout="wide"
)

# 크리처 기본 데이터 정의
creatures = {
    "토끼": {
        "hp": 30,
        "atk": 5,
        "action": 50,
        "class": "초식",
        "feature": "5% 확률로 포식자로부터 도망",
        "reproduction": "암수 한 쌍이 있을 때 70% 확률로 개체수 5~10마리 증가",
        "start_pop": 20,
    },
    "여우": {
        "hp": 40,
        "atk": 20,
        "action": 30,
        "class": "육식",
        "feature": "20% 확률로 본인이 타겟팅한 사냥감을 쫓아간다",
        "reproduction": "암수 한 쌍이 있을 때 60% 확률로 개체수 2~3마리 증가",
        "start_pop": 10,
    },
    "늑대": {
        "hp": 60,
        "atk": 30,
        "action": 60,
        "class": "육식",
        "feature": "2마리 이상 모이면 늑대 무리 형성 (우두머리 싸움)",
        "reproduction": "암수 한 쌍이 있을 때 50% 확률로 개체수 2~6마리 증가",
        "start_pop": 4,
    },
    "스컹크": {
        "hp": 50,
        "atk": 10,
        "action": 40,
        "class": "초식",
        "feature": "악성 독취 (70% 도망, 20% 변화없음, 10% 즉사)",
        "reproduction": "암수 한 쌍이 있을 때 50% 확률로 개체수 2~3마리 증가",
        "start_pop": 14,
    },
    "닭": {
        "hp": 20,
        "atk": 2,
        "action": 5,
        "class": "초식",
        "feature": "매턴 50% 확률로 알 3~10개 산란 (알 HP 5, 3턴 후 부화)",
        "reproduction": "암탉 1마리만 있어도 산란 가능",
        "start_pop": 20,
    },
}

st.title("🌲 야생 숲 생태계 시뮬레이터")
st.markdown(
    "숲 지도 위에서 크리처들이 돌아다니며 상호작용하는 시뮬레이션입니다."
)

# 사이드바 메뉴
menu = st.sidebar.selectbox("메뉴 선택", ["크리처 도감", "숲 시뮬레이션 맵"])

if menu == "크리처 도감":
    selected_name = st.sidebar.selectbox(
        "크리처를 선택하세요", list(creatures.keys())
    )
    c_data = creatures[selected_name]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"📌 {selected_name} 상세 스탯")
        st.metric(label="체력 (HP)", value=c_data["hp"])
        st.metric(label="공격력", value=c_data["atk"])
        st.metric(label="행동력", value=c_data["action"])
        st.write(f"**식성 분류:** {c_data['class']}")
    with col2:
        st.subheader("🧬 특성 및 생태 정보")
        st.info(f"**특성:** {c_data['feature']}")
        st.success(f"**번식 방식:** {c_data['reproduction']}")
        st.warning(f"**시작 개체수:** {c_data['start_pop']}마리")

elif menu == "숲 시뮬레이션 맵":
    st.subheader("🗺️ 야생 숲 실시간 이동 맵")
    st.markdown(
        "아래 버튼을 누르면 크리처들이 숲 속(10x10 격자)을 무작위로 돌아다닙니다."
    )

    # 세션 상태에 크리처 위치 초기화
    if "positions" not in st.session_state:
        st.session_state.positions = {}
        for name, data in creatures.items():
            st.session_state.positions[name] = [
                [random.randint(0, 9), random.randint(0, 9)]
                for _ in range(data["start_pop"])
            ]

    # 시뮬레이션 제어 버튼
    col_a, col_b = st.columns(2)
    with col_a:
        step_btn = st.button("🐾 한 걸음 이동하기 (Next Step)")
    with col_b:
        reset_btn = st.button("🔄 초기화하기")

    if reset_btn:
        for name, data in creatures.items():
            st.session_state.positions[name] = [
                [random.randint(0, 9), random.randint(0, 9)]
                for _ in range(data["start_pop"])
            ]
        st.rerun()

    if step_btn:
        # 모든 크리처가 상하좌우 중 한 칸으로 랜덤 이동
        for name, coords in st.session_state.positions.items():
            new_coords = []
            for x, y in coords:
                dx, dy = random.choice(
                    [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
                )
                nx = max(0, min(9, x + dx))
                ny = max(0, min(9, y + dy))
                new_coords.append([nx, ny])
            st.session_state.positions[name] = new_coords

    # 10x10 격자 맵 시각화
    grid = [["🌿 숲" for _ in range(10)] for _ in range(10)]

    icon_map = {
        "토끼": "🐰",
        "여우": "🦊",
        "늑대": "🐺",
        "스컹크": "🦨",
        "닭": "🐔",
    }

    # 맵에 크리처 표시 (여러 마리가 겹치면 아이콘 나열)
    display_grid = [["" for _ in range(10)] for _ in range(10)]
    for name, coords in st.session_state.positions.items():
        icon = icon_map.get(name, "🐾")
        for x, y in coords:
            if display_grid[x][y] == "":
                display_grid[x][y] = icon
            else:
                display_grid[x][y] += f" {icon}"

    # 표 형태로 숲 지도 출력
    table_data = []
    for i in range(10):
        row = []
        for j in range(10):
            cell = display_grid[i][j]
            row.append(cell if cell != "" else "·")
        table_data.append(row)

    import pandas as pd

    df_map = pd.DataFrame(table_data)
    st.dataframe(df_map, use_container_width=True)

    # 현재 개체수 요약
    st.markdown("### 📊 현재 생태계 개체수 현황")
    pop_cols = st.columns(len(creatures))
    idx = 0
    for name, coords in st.session_state.positions.items():
        with pop_cols[idx]:
            st.metric(label=f"{icon_map[name]} {name}", value=f"{len(coords)}마리")
        idx += 1
