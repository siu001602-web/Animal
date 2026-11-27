import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="생태계 크리처 시뮬레이터", page_icon="🐾", layout="wide"
)

# 세션 상태 초기화 (개체들의 상세 정보 및 위치 관리)
if "grid_size" not in st.session_state:
    st.session_state.grid_size = 10
    st.session_state.creatures_list = []
    cid = 1

    # 토끼 (암컷 10, 수컷 10)
    for g in ["암컷"] * 10 + ["수컷"] * 10:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "토끼",
            "x": random.randint(0, 9),
            "y": random.randint(0, 9),
            "hp": 30,
            "atk": 5,
            "action": 50,
            "gender": g,
            "status": "생존",
            "age": 0,
        })
        cid += 1

    # 여우 (암컷 5, 수컷 5)
    for g in ["암컷"] * 5 + ["수컷"] * 5:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "여우",
            "x": random.randint(0, 9),
            "y": random.randint(0, 9),
            "hp": 40,
            "atk": 20,
            "action": 30,
            "gender": g,
            "status": "생존",
            "age": 0,
        })
        cid += 1

    # 늑대 (암컷 2, 수컷 2)
    for g in ["암컷"] * 2 + ["수컷"] * 2:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "늑대",
            "x": random.randint(0, 9),
            "y": random.randint(0, 9),
            "hp": 60,
            "atk": 30,
            "action": 60,
            "gender": g,
            "status": "생존",
            "age": 0,
        })
        cid += 1

    # 스컹크 (암컷 7, 수컷 7)
    for g in ["암컷"] * 7 + ["수컷"] * 7:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "스컹크",
            "x": random.randint(0, 9),
            "y": random.randint(0, 9),
            "hp": 50,
            "atk": 10,
            "action": 40,
            "gender": g,
            "status": "생존",
            "age": 0,
        })
        cid += 1

    # 닭 (암컷 10, 수컷 10)
    for g in ["암컷"] * 10 + ["수컷"] * 10:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "닭",
            "x": random.randint(0, 9),
            "y": random.randint(0, 9),
            "hp": 20,
            "atk": 2,
            "action": 5,
            "gender": g,
            "status": "생존",
            "age": 0,
        })
        cid += 1

st.title("🌲 야생 숲 생태계 특성 시뮬레이터")
st.markdown(
    "행동력(속도)에 따른 선공권과 성별 판정, 크리처별 고유 특성이 적용된 맵입니다."
)

menu = st.sidebar.selectbox("메뉴 선택", ["숲 시뮬레이션 맵", "크리처 도감"])

if menu == "크리처 도감":
  st.subheader("📖 크리처 설정 가이드")
  st.markdown(
      """
    - **토끼**: HP 30, 공격력 5, 행동력 50 (초식) / 5% 확률로 도망 / 암수 한쌍 70% 확률 개체수 5~10마리 증가 (성별 랜덤)
    - **여우**: HP 40, 공격력 20, 행동력 30 (육식) / 20% 확률로 사냥감 추적 / 암수 한쌍 60% 확률 개체수 2~3마리 증가 (성별 랜덤)
    - **늑대**: HP 60, 공격력 30, 행동력 60 (육식) / 무리 형성 및 우두머리 결투 (패배 시 사망) / 암수 한쌍 50% 확률 개체수 2~6마리 증가
    - **스컹크**: HP 50, 공격력 10, 행동력 40 (초식) / 70% 도망감, 20% 변화없음, 10% 포식자 즉사 / 암수 한쌍 50% 확률 개체수 2~3마리 증가
    - **닭**: HP 20, 공격력 2, 행동력 5 (초식) / 암탉 1마리만 있어도 매턴 50% 확률로 알 3~10개 산란 (알 HP 5, 3턴 후 부화)
    """
  )

elif menu == "숲 시뮬레이션 맵":
  col_a, col_b = st.columns(2)
  with col_a:
    step_btn = st.button("🐾 1턴 진행하기 (Next Turn)")
  with col_b:
    reset_btn = st.button("🔄 시뮬레이션 초기화")

  if reset_btn:
    st.session_state.clear()
    st.rerun()

  if step_btn:
    living_creatures = [
        c for c in st.session_state.creatures_list if c["status"] == "생존"
    ]
    living_creatures.sort(key=lambda x: x["action"], reverse=True)

    event_logs = []

    # 1. 이동 및 개별 특성 처리 (산란, 성장 등)
    for c in living_creatures:
      if c["status"] != "생존":
        continue

      # 무작위 이동
      dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)])
      c["x"] = max(0, min(9, c["x"] + dx))
      c["y"] = max(0, min(9, c["y"] + dy))

      # 닭 산란 (암탉 1마리만 있어도 매턴 50% 확률로 알 3~10개)
      if c["type"] == "닭" and c["gender"] == "암컷":
        if random.random() < 0.5:
          egg_count = random.randint(3, 10)
          for _ in range(egg_count):
            st.session_state.creatures_list.append({
                "id": len(st.session_state.creatures_list) + 1,
                "type": "알",
                "x": c["x"],
                "y": c["y"],
                "hp": 5,
                "atk": 0,
                "action": 0,
                "gender": "중성",
                "status": "생존",
                "age": 0,
            })
          event_logs.append(
              f"🐔 닭이 좌표 ({c['x']}, {c['y']})에 알 {egg_count}개를 산란했습니다!"
          )

      # 알 부화 (3턴 후)
      if c["type"] == "알":
        c["age"] += 1
        if c["age"] >= 3:
          c["type"] = "병아리"
          c["hp"] = 10
          c["action"] = 3
          event_logs.append(
              f"🥚 알이 부화하여 병아리가 되었습니다! (좌표: {c['x']}, {c['y']})"
          )

      # 병아리 성장 (5턴 후 닭)
      if c["type"] == "병아리":
        c["age"] += 1
        if c["age"] >= 5:
          c["type"] = "닭"
          c["hp"] = 20
          c["action"] = 5
          event_logs.append(
              f"🐥 병아리가 성장하여 닭이 되었습니다! (좌표: {c['x']}, {c['y']})"
          )

    # 2. 같은 칸에 모인 개체들 간의 번식 및 전투 처리
    positions_map = {}
    for c in st.session_state.creatures_list:
      if c["status"] == "생존":
        pos_key = (c["x"], c["y"])
        if pos_key not in positions_map:
          positions_map[pos_key] = []
        positions_map[pos_key].append(c)

    for pos, group in positions_map.items():
      # 번식 체크 (같은 칸에 암컷과 수컷이 함께 있는 경우)
      types_in_group = set(c["type"] for c in group)
      for t_name in types_in_group:
        if t_name in ["토끼", "여우", "늑대", "스컹크"]:
          sub_group = [c for c in group if c["type"] == t_name]
          has_female = any(c["gender"] == "암컷" for c in sub_group)
          has_male = any(c["gender"] == "수컷" for c in sub_group)

          if has_female and has_male:
            # 토끼: 70% 확률로 5~10마리 증가
            if t_name == "토끼" and random.random() < 0.7:
              inc = random.randint(5, 10)
              for _ in range(inc):
                st.session_state.creatures_list.append({
                    "id": len(st.session_state.creatures_list) + 1,
                    "type": "토끼",
                    "x": pos[0],
                    "y": pos[1],
                    "hp": 30,
                    "atk": 5,
                    "action": 50,
                    "gender": random.choice(["암컷", "수컷"]),
                    "status": "생존",
                    "age": 0,
                })
              event_logs.append(
                  f"🐰 토끼 커플 번식 성공! 개체수 {inc}마리 증가 (좌표:"
                  f" {pos})"
              )

            # 여우: 60% 확률로 2~3마리 증가
            elif t_name == "여우" and random.random() < 0.6:
              inc = random.randint(2, 3)
              for _ in range(inc):
                st.session_state.creatures_list.append({
                    "id": len(st.session_state.creatures_list) + 1,
                    "type": "여우",
                    "x": pos[0],
                    "y": pos[1],
                    "hp": 40,
                    "atk": 20,
                    "action": 30,
                    "gender": random.choice(["암컷", "수컷"]),
                    "status": "생존",
                    "age": 0,
                })
              event_logs.append(
                  f"🦊 여우 커플 번식 성공! 개체수 {inc}마리 증가 (좌표:"
                  f" {pos})"
              )

            # 늑대: 50% 확률로 2~6마리 증가
            elif t_name == "늑대" and random.random() < 0.5:
              inc = random.randint(2, 6)
              for _ in range(inc):
                st.session_state.creatures_list.append({
                    "id": len(st.session_state.creatures_list) + 1,
                    "type": "늑대",
                    "x": pos[0],
                    "y": pos[1],
                    "hp": 60,
                    "atk": 30,
                    "action": 60,
                    "gender": random.choice(["암컷", "수컷"]),
                    "status": "생존",
                    "age": 0,
                })
              event_logs.append(
                  f"🐺 늑대 커플 번식 성공! 개체수 {inc}마리 증가 (좌표:"
                  f" {pos})"
              )

            # 스컹크: 50% 확률로 2~3마리 증가
            elif t_name == "스컹크" and random.random() < 0.5:
              inc = random.randint(2, 3)
              for _ in range(inc):
                st.session_state.creatures_list.append({
                    "id": len(st.session_state.creatures_list) + 1,
                    "type": "스컹크",
                    "x": pos[0],
                    "y": pos[1],
                    "hp": 50,
                    "atk": 10,
                    "action": 40,
                    "gender": random.choice(["암컷", "수컷"]),
                    "status": "생존",
                    "age": 0,
                })
              event_logs.append(
                  f"🦨 스컹크 커플 번식 성공! 개체수 {inc}마리 증가 (좌표:"
                  f" {pos})"
              )

      # 전투 및 포식 상호작용
      predators = [c for c in group if c["type"] in ["여우", "늑대"]]
      preys = [
          c for c in group if c["type"] in ["토끼", "스컹크", "닭", "알", "병아리"]
      ]

      if predators and preys:
        for pred in predators:
          for prey in preys:
            if prey["status"] != "생존":
              continue

            # 토끼 도망 특성 (5%)
            if prey["type"] == "토끼" and random.random() < 0.05:
              event_logs.append(
                  f"🐰 토끼가 포식자({pred['type']})를 보고 도망쳤습니다!"
              )
              continue

            # 스컹크 독가스 특성
            if prey["type"] == "스컹크":
              sk_rand = random.random()
              if sk_rand < 0.7:
                event_logs.append(
                    f"🦨 스컹크의 악취 독가스! 포식자({pred['type']})가 도망쳤습니다."
                )
                continue
              elif sk_rand < 0.9:
                pass
              else:
                pred["status"] = "사망"
                event_logs.append(
                    f"💀 스컹크의 치명적인 독가스로 포식자({pred['type']}) 즉사!"
                )
                break

            # 행동력 비교 선공
            if pred["action"] >= prey["action"]:
              prey["hp"] -= pred["atk"]
              if prey["hp"] <= 0:
                prey["status"] = "사망"
                event_logs.append(
                    f"⚔️ {pred['type']}(행동력 {pred['action']})이(가)"
                    f" {prey['type']}을(를) 사냥했습니다!"
                )

      # 늑대 우두머리 결투
      wolves = [c for c in group if c["type"] == "늑대" and c["status"] == "생존"]
      if len(wolves) >= 2:
        w1, w2 = wolves[0], wolves[1]
        if w1["action"] >= w2["action"]:
          w2["status"] = "사망"
          event_logs.append(
              "👑 늑대 우두머리 결투! 패배한 우두머리 늑대가 사망했습니다."
          )
        else:
          w1["status"] = "사망"
          event_logs.append(
              "👑 늑대 우두머리 결투! 패배한 우두머리 늑대가 사망했습니다."
          )

    st.session_state.event_logs = event_logs

  # 10x10 격자 맵 시각화
  icon_map = {
      "토끼": "🐰",
      "여우": "🦊",
      "늑대": "🐺",
      "스컹크": "🦨",
      "닭": "🐔",
      "병아리": "🐥",
      "알": "🥚",
  }

  display_grid = [["" for _ in range(10)] for _ in range(10)]
  for c in st.session_state.creatures_list:
    if c["status"] == "생존":
      icon = icon_map.get(c["type"], "🐾")
      x, y = c["x"], c["y"]
      if display_grid[x][y] == "":
        display_grid[x][y] = icon
      else:
        display_grid[x][y] += f" {icon}"

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

  # 이벤트 로그
  st.markdown("### 📜 이번 턴 생태계 이벤트 로그")
  if "event_logs" in st.session_state and st.session_state.event_logs:
    for log in st.session_state.event_logs[-10:]:
      st.write(log)
  else:
    st.info("상단의 '1턴 진행하기' 버튼을 눌러 시뮬레이션을 시작해보세요!")

  # 하단 생존 개체수 현황 (암컷/수컷 마릿수 상세 표시)
  st.markdown("### 📊 생존 개체수 현황 (암수 상세)")
  alive_stats = {}
  for c in st.session_state.creatures_list:
    if c["status"] == "생존":
      t = c["type"]
      g = c["gender"]
      if t not in alive_stats:
        alive_stats[t] = {"암컷": 0, "수컷": 0, "중성": 0}
      if g in alive_stats[t]:
        alive_stats[t][g] += 1

  cols = st.columns(len(icon_map))
  idx = 0
  for t_name, t_icon in icon_map.items():
    if idx < len(cols):
      with cols[idx]:
        stats = alive_stats.get(
            t_name, {"암컷": 0, "수컷": 0, "중성": 0}
        )
        if t_name in ["알"]:
          st.metric(label=f"{t_icon} {t_name}", value=f"{stats['중성']}개")
        else:
          st.metric(
              label=f"{t_icon} {t_name}",
              value=f"♀ {stats['암컷']} / ♂ {stats['수컷']}",
          )
      idx += 1
