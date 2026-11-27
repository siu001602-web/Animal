import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="생태계 크리처 시뮬레이터", page_icon="🐾", layout="centered"
)

# 세션 상태 초기화 (5x5 지도)
if "grid_size" not in st.session_state:
    st.session_state.grid_size = 5
    st.session_state.creatures_list = []
    # 산불 상태 그리드 초기화 (False: 정상, True: 산불 발생)
    st.session_state.fires = [[False for _ in range(5)] for _ in range(5)]
    cid = 1

    # 토끼 (암컷 10, 수컷 10)
    for g in ["암컷"] * 10 + ["수컷"] * 10:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "토끼",
            "x": random.randint(0, 4),
            "y": random.randint(0, 4),
            "hp": 30,
            "atk": 5,
            "action": 50,
            "gender": g,
            "status": "생존",
            "age": 0,
            "is_new": False,
            "hunger_timer": 0,
            "dead_turns": 0,
        })
        cid += 1

    # 여우 (암컷 5, 수컷 5)
    for g in ["암컷"] * 5 + ["수컷"] * 5:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "여우",
            "x": random.randint(0, 4),
            "y": random.randint(0, 4),
            "hp": 40,
            "atk": 20,
            "action": 30,
            "gender": g,
            "status": "생존",
            "age": 0,
            "is_new": False,
            "hunger_timer": 0,
            "dead_turns": 0,
        })
        cid += 1

    # 늑대 (암컷 2, 수컷 2)
    for g in ["암컷", "암컷", "수컷", "수컷"]:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "늑대",
            "x": random.randint(0, 4),
            "y": random.randint(0, 4),
            "hp": 60,
            "atk": 30,
            "action": 60,
            "gender": g,
            "status": "생존",
            "age": 0,
            "pack_id": cid,
            "is_new": False,
            "hunger_timer": 0,
            "dead_turns": 0,
        })
        cid += 1

    # 스컹크 (암컷 7, 수컷 7)
    for g in ["암컷"] * 7 + ["수컷"] * 7:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "스컹크",
            "x": random.randint(0, 4),
            "y": random.randint(0, 4),
            "hp": 50,
            "atk": 10,
            "action": 40,
            "gender": g,
            "status": "생존",
            "age": 0,
            "is_new": False,
            "hunger_timer": 0,
            "dead_turns": 0,
        })
        cid += 1

    # 닭 (암컷 10, 수컷 10)
    for g in ["암컷"] * 10 + ["수컷"] * 10:
        st.session_state.creatures_list.append({
            "id": cid,
            "type": "닭",
            "x": random.randint(0, 4),
            "y": random.randint(0, 4),
            "hp": 20,
            "atk": 2,
            "action": 5,
            "gender": g,
            "status": "생존",
            "age": 0,
            "is_new": False,
            "hunger_timer": 0,
            "dead_turns": 0,
        })
        cid += 1

st.title("🌲 야생 숲 생태계 시뮬레이터")
st.markdown(
    "5×5 숲 지도에서 크리처들의 생존, **산불, 배고픔(기아), 시체 부패**를"
    " 관찰하세요!"
)

menu = st.sidebar.selectbox("메뉴 선택", ["숲 시뮬레이션 맵", "크리처 도감"])

icon_map = {
    "토끼": "🐰",
    "여우": "🦊",
    "늑대": "🐺",
    "스컹크": "🦨",
    "닭": "🐔",
    "병아리": "🐥",
    "알": "🥚",
    "시체": "💀",
}


def get_creature_icon(c):
    if c["status"] == "사망":
        return "💀"

    c_type = c["type"]
    gender = c["gender"]
    is_new = c.get("is_new", False)
    new_mark = "✨" if is_new else ""

    if c_type == "토끼":
        base = "🐰♀" if gender == "암컷" else "🐰♂"
    elif c_type == "여우":
        base = "🦊♀" if gender == "암컷" else "🦊♂"
    elif c_type == "늑대":
        base = "🐺♀" if gender == "암컷" else "🐺♂"
    elif c_type == "스컹크":
        base = "🦨♀" if gender == "암컷" else "🦨♂"
    elif c_type == "닭":
        base = "🐔♀" if gender == "암컷" else "🐔♂"
    elif c_type == "병아리":
        base = "🐥♀" if gender == "암컷" else "🐥♂"
    elif c_type == "알":
        base = "🥚"
    else:
        base = "🐾"

    return f"{base}{new_mark}"


if menu == "크리처 도감":
    st.subheader("📖 크리처, 재난 및 생존 규칙 가이드")
    st.markdown(
        """
    - **초식동물(토끼, 스컹크, 닭, 병아리)**: 매 턴 지역별 **70% 확률로 자라는 풀**을 먹어야 합니다. 3턴 동안 풀을 먹지 못하면 아사(사망)합니다.
    - **포식자(여우, 늑대)**: 3턴 동안 사냥 및 먹이 섭취를 하지 못하면 아사(사망)합니다.
    - **달걀 규칙**: 산란 다음 턴에 병아리로 부화하며, 부서지더라도 **시체(💀)가 남지 않고 한 번에 최대 3개까지만** 부서집니다.
    - **산불 시스템**: 
      - 매 턴 각 지역마다 **1% 확률**로 자연발화 발생, 인접 지역으로 **1% 확률** 확산
      - 산불이 난 지역에 있는 **모든 동물은 즉사**하며 해당 지역은 이용 불가
    - **시체 시스템**: 
      - 사망한 동물은 **해골(💀) 이모티콘**으로 지도에 **3턴 동안** 남았다가 부패하여 사라집니다.
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
        for c in st.session_state.creatures_list:
            if c["status"] == "생존":
                c["is_new"] = False

        event_logs = []

        # --- [1. 산불 시스템 처리] ---
        new_fires = [
            [st.session_state.fires[i][j] for j in range(5)] for i in range(5)
        ]

        for i in range(5):
            for j in range(5):
                if not st.session_state.fires[i][j]:
                    if random.random() < 0.01:
                        new_fires[i][j] = True
                        event_logs.append(
                            f"🔥 경고! 좌표 ({i}, {j})에 산불이 발생했습니다!"
                        )
                    else:
                        neighbors = [
                            (i - 1, j),
                            (i + 1, j),
                            (i, j - 1),
                            (i, j + 1),
                        ]
                        adjacent_on_fire = any(
                            0 <= ni < 5
                            and 0 <= nj < 5
                            and st.session_state.fires[ni][nj]
                            for ni, nj in neighbors
                        )
                        if adjacent_on_fire and random.random() < 0.01:
                            new_fires[i][j] = True
                            event_logs.append(
                                f"🔥 산불이 인접 지역 ({i}, {j})(으)로 번졌습니다!"
                            )

        # 산불 난 지역에 있는 개체 즉사 처리 (달걀은 해골 없이 바로 소멸)
        for i in range(5):
            for j in range(5):
                if not st.session_state.fires[i][j] and new_fires[i][j]:
                    for c in st.session_state.creatures_list:
                        if c["status"] == "생존" and c["x"] == i and c["y"] == j:
                            if c["type"] == "알":
                                c["status"] = "부패됨"
                            else:
                                c["status"] = "사망"
                                c["dead_turns"] = 0
                                event_logs.append(
                                    f"🔥 크리처({c['type']})가 산불에 휩쓸려 즉사했습니다!"
                                )

        st.session_state.fires = new_fires

        # --- [2. 지역별 풀 생성 (70% 확률)] ---
        grass_map = {}
        for i in range(5):
            for j in range(5):
                if not st.session_state.fires[i][j]:
                    if random.random() < 0.70:
                        grass_map[(i, j)] = True

        living_creatures = [
            c for c in st.session_state.creatures_list if c["status"] == "생존"
        ]
        living_creatures.sort(key=lambda x: x["action"], reverse=True)

        # 늑대 무리 이동 방향
        pack_moves = {}
        for c in living_creatures:
            if c["type"] == "늑대":
                pid = c.get("pack_id", c["id"])
                if pid not in pack_moves:
                    pack_moves[pid] = random.choice(
                        [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
                    )

        # --- [3. 이동 및 풀/사냥 기아 타이머 처리] ---
        for c in living_creatures:
            if c["status"] != "생존":
                continue

            if c["type"] == "늑대":
                pid = c.get("pack_id", c["id"])
                dx, dy = pack_moves[pid]
                nx = max(0, min(4, c["x"] + dx))
                ny = max(0, min(4, c["y"] + dy))
                if not st.session_state.fires[nx][ny]:
                    c["x"], c["y"] = nx, ny
            elif c["type"] != "알":
                moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
                random.shuffle(moves)
                for dx, dy in moves:
                    nx = max(0, min(4, c["x"] + dx))
                    ny = max(0, min(4, c["y"] + dy))
                    if not st.session_state.fires[nx][ny]:
                        c["x"], c["y"] = nx, ny
                        break

            # 초식동물 풀 섭취 체크
            if c["type"] in ["토끼", "스컹크", "닭", "병아리"]:
                if (c["x"], c["y"]) in grass_map:
                    c["hunger_timer"] = 0
                else:
                    c["hunger_timer"] += 1
                    if c["hunger_timer"] >= 3:
                        c["status"] = "사망"
                        c["dead_turns"] = 0
                        event_logs.append(
                            f"🌾 초식동물({c['type']})이 3턴 동안 풀을 먹지 못해 굶어 죽었습니다!"
                        )

            # 닭 산란 (암컷만, 20% 확률)
            if c["type"] == "닭" and c["gender"] == "암컷":
                if (
                    not st.session_state.fires[c["x"]][c["y"]]
                    and random.random() < 0.20
                ):
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
                            "is_new": True,
                            "hunger_timer": 0,
                            "dead_turns": 0,
                        })
                    event_logs.append(
                        f"🐔 암컷 닭이 ({c['x']}, {c['y']})에 알 {egg_count}개를 산란했습니다!"
                    )

            # 알 부화 처리 (바로 다음 턴)
            elif c["type"] == "알":
                c["age"] += 1
                if c["age"] >= 1:
                    c["type"] = "병아리"
                    c["hp"] = 10
                    c["action"] = 3
                    c["age"] = 0
                    c["gender"] = random.choice(["암컷", "수컷"])
                    c["is_new"] = True
                    c["hunger_timer"] = 0
                    event_logs.append(
                        f"🥚 알이 부화하여 병아리({c['gender']})가 되었습니다! ({c['x']}, {c['y']})"
                    )

            # 병아리 성장 (3턴 후 닭)
            elif c["type"] == "병아리":
                c["age"] += 1
                if c["age"] >= 3:
                    c["type"] = "닭"
                    c["hp"] = 20
                    c["action"] = 5
                    c["age"] = 0
                    c["is_new"] = True
                    event_logs.append(
                        f"🐥 병아리가 성장하여 ({c['x']}, {c['y']}) 닭({c['gender']})이 되었습니다!"
                    )

        # --- [4. 같은 칸 상호작용 (번식 및 사냥/기아 리셋)] ---
        positions_map = {}
        for c in st.session_state.creatures_list:
            if c["status"] == "생존":
                pos_key = (c["x"], c["y"])
                if pos_key not in positions_map:
                    positions_map[pos_key] = []
                positions_map[pos_key].append(c)

        for pos, group in positions_map.items():
            if st.session_state.fires[pos[0]][pos[1]]:
                continue

            # 늑대 무리 결성 및 우두머리 결투
            wolves = [c for c in group if c["type"] == "늑대" and c["status"] == "생존"]
            if len(wolves) >= 2:
                packs = {}
                for w in wolves:
                    pid = w.get("pack_id", w["id"])
                    if pid not in packs:
                        packs[pid] = []
                    packs[pid].append(w)

                if len(packs) >= 2:
                    pack_ids = list(packs.keys())
                    all_living_wolves = [
                        w
                        for w in st.session_state.creatures_list
                        if w["type"] == "늑대" and w["status"] == "생존"
                    ]
                    pack_sizes = {
                        pid: sum(
                            1
                            for w in all_living_wolves
                            if w.get("pack_id", w["id"]) == pid
                        )
                        for pid in pack_ids
                    }
                    actual_packs = [
                        pid for pid in pack_ids if pack_sizes[pid] >= 2
                    ]

                    if len(actual_packs) >= 2:
                        p1, p2 = actual_packs[0], actual_packs[1]
                        winner_pid, loser_pid = random.sample([p1, p2], 2)
                        loser_leader = packs[loser_pid][0]
                        loser_leader["status"] = "사망"
                        loser_leader["dead_turns"] = 0

                        for w in all_living_wolves:
                            if (
                                w["status"] == "생존"
                                and w.get("pack_id", w["id"]) == loser_pid
                            ):
                                w["pack_id"] = winner_pid

                        event_logs.append(
                            f"👑 늑대 무리 충돌({pos})! 우두머리 결투 끝에 패배한 우두머리가 사망하고 무리가 흡수되었습니다."
                        )
                    else:
                        target_pid = (
                            actual_packs[0] if actual_packs else pack_ids[0]
                        )
                        for w in wolves:
                            w["pack_id"] = target_pid
                        event_logs.append(
                            f"🐺 늑대들이 {pos}에서 만나 늑대 무리를 형성했습니다!"
                        )

            # 번식 체크
            types_in_group = set(c["type"] for c in group)
            for t_name in types_in_group:
                if t_name in ["토끼", "여우", "늑대", "스컹크"]:
                    sub_group = [
                        c
                        for c in group
                        if c["type"] == t_name and c["status"] == "생존"
                    ]
                    has_female = any(c["gender"] == "암컷" for c in sub_group)
                    has_male = any(c["gender"] == "수컷" for c in sub_group)

                    if has_female and has_male:
                        if t_name == "토끼" and random.random() < 0.30:
                            inc = random.randint(5, 10)
                            for _ in range(inc):
                                st.session_state.creatures_list.append({
                                    "id": len(st.session_state.creatures_list) + 1,
                                    "type": "토끼",
                                    "x": random.randint(0, 4),
                                    "y": random.randint(0, 4),
                                    "hp": 30,
                                    "atk": 5,
                                    "action": 50,
                                    "gender": random.choice(["암컷", "수컷"]),
                                    "status": "생존",
                                    "age": 0,
                                    "is_new": True,
                                    "hunger_timer": 0,
                                    "dead_turns": 0,
                                })
                            event_logs.append(f"🐰 토끼 번식 성공! +{inc}마리")

                        elif t_name == "여우" and random.random() < 0.6:
                            inc = random.randint(2, 3)
                            for _ in range(inc):
                                st.session_state.creatures_list.append({
                                    "id": len(st.session_state.creatures_list) + 1,
                                    "type": "여우",
                                    "x": random.randint(0, 4),
                                    "y": random.randint(0, 4),
                                    "hp": 40,
                                    "atk": 20,
                                    "action": 30,
                                    "gender": random.choice(["암컷", "수컷"]),
                                    "status": "생존",
                                    "age": 0,
                                    "is_new": True,
                                    "hunger_timer": 0,
                                    "dead_turns": 0,
                                })
                            event_logs.append(f"🦊 여우 번식 성공! +{inc}마리")

                        elif t_name == "늑대" and random.random() < 0.5:
                            inc = random.randint(2, 6)
                            parent_pack_id = sub_group[0].get(
                                "pack_id", sub_group[0]["id"]
                            )
                            for _ in range(inc):
                                st.session_state.creatures_list.append({
                                    "id": len(st.session_state.creatures_list) + 1,
                                    "type": "늑대",
                                    "x": random.randint(0, 4),
                                    "y": random.randint(0, 4),
                                    "hp": 60,
                                    "atk": 30,
                                    "action": 60,
                                    "gender": random.choice(["암컷", "수컷"]),
                                    "status": "생존",
                                    "age": 0,
                                    "pack_id": parent_pack_id,
                                    "is_new": True,
                                    "hunger_timer": 0,
                                    "dead_turns": 0,
                                })
                            event_logs.append(f"🐺 늑대 번식 성공! +{inc}마리")

                        elif t_name == "스컹크" and random.random() < 0.5:
                            inc = random.randint(2, 3)
                            for _ in range(inc):
                                st.session_state.creatures_list.append({
                                    "id": len(st.session_state.creatures_list) + 1,
                                    "type": "스컹크",
                                    "x": random.randint(0, 4),
                                    "y": random.randint(0, 4),
                                    "hp": 50,
                                    "atk": 10,
                                    "action": 40,
                                    "gender": random.choice(["암컷", "수컷"]),
                                    "status": "생존",
                                    "age": 0,
                                    "is_new": True,
                                    "hunger_timer": 0,
                                    "dead_turns": 0,
                                })
                            event_logs.append(f"🦨 스컹크 번식 성공! +{inc}마리")

            # 육식동물끼리의 전투 (늑대 vs 여우)
            living_wolves = [c for c in group if c["type"] == "늑대" and c["status"] == "생존"]
            living_foxes = [c for c in group if c["type"] == "여우" and c["status"] == "생존"]
            if living_wolves and living_foxes:
                for w in living_wolves:
                    w["hunger_timer"] = 0
                    for f in living_foxes:
                        if f["status"] != "생존":
                            continue
                        f["hp"] -= w["atk"]
                        if f["hp"] <= 0:
                            f["status"] = "사망"
                            f["dead_turns"] = 0
                            event_logs.append(f"🐺⚔️🦊 늑대가 여우를 사냥했습니다! ({pos})")

            # 포식자 vs 초식/알 사냥 처리
            predators = [
                c
                for c in group
                if c["type"] in ["여우", "늑대"] and c["status"] == "생존"
            ]
            preys = [
                c
                for c in group
                if c["type"] in ["토끼", "스컹크", "닭", "알", "병아리"]
                and c["status"] == "생존"
            ]

            if predators and preys:
                eggs_broken_in_cell = 0  # 이 칸에서 이번 턴에 깨진 달걀 수 카운트 (최대 3개 제한)
                for pred in predators:
                    if pred["status"] != "생존":
                        continue
                    pred["hunger_timer"] = 0

                    for prey in preys:
                        if prey["status"] != "생존":
                            continue

                        # 달걀은 한 턴에 한 칸에서 최대 3개까지만 부서질 수 있음
                        if prey["type"] == "알" and eggs_broken_in_cell >= 3:
                            continue

                        if prey["type"] == "토끼" and random.random() < 0.05:
                            event_logs.append("🐰 토끼가 도망쳤습니다!")
                            continue

                        # 스컹크 독가스 (75% 도망, 20% 변화없음, 5% 즉사)
                        if prey["type"] == "스컹크":
                            sk_rand = random.random()
                            if sk_rand < 0.75:
                                event_logs.append("🦨 스컹크 악취! 포식자가 도망쳤습니다.")
                                continue
                            elif sk_rand < 0.95:
                                pass
                            else:
                                pred["status"] = "사망"
                                pred["dead_turns"] = 0
                                event_logs.append(
                                    f"💀 스컹크 독가스로 포식자({pred['type']}) 즉사!"
                                )
                                break

                        if pred["action"] >= prey["action"]:
                            prey["hp"] -= pred["atk"]
                            if prey["hp"] <= 0:
                                if prey["type"] == "알":
                                    prey["status"] = "부패됨"  # 해골 표시 없이 즉시 소멸
                                    eggs_broken_in_cell += 1
                                    event_logs.append(
                                        f"🥚 {pred['type']}이(가) 알을 깨뜨려 먹었습니다! ({pos}, 누적 {eggs_broken_in_cell}개)"
                                    )
                                else:
                                    prey["status"] = "사망"
                                    prey["dead_turns"] = 0
                                    event_logs.append(
                                        f"⚔️ {pred['type']}이(가) {prey['type']}을(를) 사냥했습니다!"
                                    )
            else:
                for pred in predators:
                    pred["hunger_timer"] += 1
                    if pred["hunger_timer"] >= 3:
                        pred["status"] = "사망"
                        pred["dead_turns"] = 0
                        event_logs.append(
                            f"🍖 포식자({pred['type']})가 3턴 동안 사냥을 하지 못해 아사했습니다!"
                        )

        # --- [5. 시체(💀) 3턴 유지 후 부패(삭제) 처리] ---
        for c in st.session_state.creatures_list:
            if c["status"] == "사망":
                c["dead_turns"] += 1
                if c["dead_turns"] >= 3:
                    c["status"] = "부패됨"

        st.session_state.event_logs = event_logs

    # 5x5 숲 지도 시각화
    display_grid = [["" for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if st.session_state.fires[i][j]:
                display_grid[i][j] = "🔥"

    for c in st.session_state.creatures_list:
        if c["status"] in ["생존", "사망"]:
            x = max(0, min(4, c["x"]))
            y = max(0, min(4, c["y"]))
            if not st.session_state.fires[x][y]:
                icon = get_creature_icon(c)
                if display_grid[x][y] == "":
                    display_grid[x][y] = icon
                else:
                    display_grid[x][y] += f" {icon}"

    st.markdown(
        "### 🗺️ 숲 구역 지도 (🔥 산불 / 💀 시체 3턴 유지 / ✨ 신생 개체)"
    )
    for i in range(5):
        cols = st.columns(5)
        for j in range(5):
            with cols[j]:
                content = display_grid[i][j]
                if content == "":
                    content = "🌲"
                st.info(content)

    # 이벤트 로그
    st.markdown("### 📜 이번 턴 이벤트 로그")
    if "event_logs" in st.session_state and st.session_state.event_logs:
        for log in st.session_state.event_logs[-7:]:
            st.write(log)
    else:
        st.info("상단의 '1턴 진행하기' 버튼을 눌러보세요!")

    # 하단 생존 개체수 현황
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

    stat_cols = st.columns(len(icon_map) - 1)
    idx = 0
    for t_name, t_icon in icon_map.items():
        if t_name == "시체":
            continue
        if idx < len(stat_cols):
            with stat_cols[idx]:
                stats = alive_stats.get(t_name, {"암컷": 0, "수컷": 0, "중성": 0})
                st.markdown(f"**{t_icon} {t_name}**")
                if t_name in ["알"]:
                    st.text(f"{stats['중성']}개")
                else:
                    st.text(f"♀{stats['암컷']} / ♂{stats['수컷']}")
            idx += 1
