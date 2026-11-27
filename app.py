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
        })
        cid += 1

    # 늑대 (암컷 2, 수컷 2 - 각자 흩어져서 시작)
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
        })
        cid += 1

st.title("🌲 야생 숲 생태계 시뮬레이터")
st.markdown(
    "5×5 숲 지도에서 크리처들의 성별(♀/♂)과 신생 개체(✨)를 관찰하세요!"
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
}


def get_creature_icon(c):
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
    st.subheader("📖 크리처 설정 가이드")
    st.markdown(
        """
    - **토끼**: HP 30, 공격력 5, 행동력 50 (초식) / 5% 도망 / 암수 한쌍 30% (5~10마리 증가)
    - **여우**: HP 40, 공격력 20, 행동력 30 (육식) / 20% 사냥감 추적 / 암수 한쌍 60% (2~3마리 증가)
    - **늑대**: HP 60, 공격력 30, 행동력 60 (육식) / 만나면 무리 형성 / 무리끼리 만나면 우두머리 결투 / **여우와 만나면 사냥**
    - **스컹크**: HP 50, 공격력 10, 행동력 40 (초식) / 70% 도망, 20% 변화없음, 10% 즉사
    - **닭**: HP 20, 공격력 2, 행동력 5 (초식) / 암컷만 20% 확률로 알 3~10개 산란 (알 HP 5, 3턴 후 부화)
    - **✨ 표시**: 새로 태어난 신생 개체(NEW)
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

        living_creatures = [
            c for c in st.session_state.creatures_list if c["status"] == "생존"
        ]
        living_creatures.sort(key=lambda x: x["action"], reverse=True)

        event_logs = []

        # 늑대 무리(pack_id)별 이동 방향
        pack_moves = {}
        for c in living_creatures:
            if c["type"] == "늑대":
                pid = c.get("pack_id", c["id"])
                if pid not in pack_moves:
                    pack_moves[pid] = random.choice(
                        [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
                    )

        # 1. 이동 및 성장/부화 처리
        for c in living_creatures:
            if c["status"] != "생존":
                continue

            if c["type"] == "늑대":
                pid = c.get("pack_id", c["id"])
                dx, dy = pack_moves[pid]
                c["x"] = max(0, min(4, c["x"] + dx))
                c["y"] = max(0, min(4, c["y"] + dy))
            elif c["type"] != "알":  # 알은 움직이지 않음
                dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)])
                c["x"] = max(0, min(4, c["x"] + dx))
                c["y"] = max(0, min(4, c["y"] + dy))

            # 닭 산란 (암컷만, 20% 확률)
            if c["type"] == "닭" and c["gender"] == "암컷":
                if random.random() < 0.20:
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
                        })
                    event_logs.append(
                        f"🐔 암컷 닭이 ({c['x']}, {c['y']})에 알 {egg_count}개를 산란했습니다!"
                    )

            # 알 부화 (3턴 후 병아리로 변하며 성별 즉시 부여)
            elif c["type"] == "알":
                c["age"] += 1
                if c["age"] >= 3:
                    c["type"] = "병아리"
                    c["hp"] = 10
                    c["action"] = 3
                    c["age"] = 0
                    c["gender"] = random.choice(["암컷", "수컷"])
                    c["is_new"] = True
                    event_logs.append(
                        f"🥚 알이 부화하여 병아리({c['gender']})가 되었습니다! ({c['x']}, {c['y']})"
                    )

            # 병아리 성장 (5턴 후 닭)
            elif c["type"] == "병아리":
                c["age"] += 1
                if c["age"] >= 5:
                    c["type"] = "닭"
                    c["hp"] = 20
                    c["action"] = 5
                    c["is_new"] = True
                    event_logs.append(
                        f"🐥 병아리가 성장하여 ({c['x']}, {c['y']}) 닭({c['gender']})이 되었습니다!"
                    )

        # 2. 같은 칸 상호작용
        positions_map = {}
        for c in st.session_state.creatures_list:
            if c["status"] == "생존":
                pos_key = (c["x"], c["y"])
                if pos_key not in positions_map:
                    positions_map[pos_key] = []
                positions_map[pos_key].append(c)

        for pos, group in positions_map.items():
            # 늑대 무리 결성 및 무리 간 우두머리 싸움
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
                            f"🐺 늑대들이 {pos}에서 만나 늑대 무리를 형성했습니다! (총 {len(wolves)}마리 동행)"
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
                                })
                            event_logs.append(f"🦨 스컹크 번식 성공! +{inc}마리")

            # 육식동물끼리의 전투 (늑대 vs 여우)
            living_wolves = [c for c in group if c["type"] == "늑대" and c["status"] == "생존"]
            living_foxes = [c for c in group if c["type"] == "여우" and c["status"] == "생존"]
            if living_wolves and living_foxes:
                for w in living_wolves:
                    for f in living_foxes:
                        if f["status"] != "생존":
                            continue
                        # 늑대 행동력(60) > 여우 행동력(30) 이므로 늑대가 선공
                        f["hp"] -= w["atk"]
                        if f["hp"] <= 0:
                            f["status"] = "사망"
                            event_logs.append(f"🐺⚔️🦊 늑대가 여우를 공격해 사냥했습니다! ({pos})")

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
                for pred in predators:
                    if pred["status"] != "생존":
                        continue
                    for prey in preys:
                        if prey["status"] != "생존":
                            continue

                        if prey["type"] == "토끼" and random.random() < 0.05:
                            event_logs.append("🐰 토끼가 도망쳤습니다!")
                            continue

                        if prey["type"] == "스컹크":
                            sk_rand = random.random()
                            if sk_rand < 0.7:
                                event_logs.append("🦨 스컹크 독가스! 포식자가 도망쳤습니다.")
                                continue
                            elif sk_rand >= 0.9:
                                pred["status"] = "사망"
                                event_logs.append(
                                    f"💀 스컹크 독가스로 포식자({pred['type']}) 즉사!"
                                )
                                break

                        if pred["action"] >= prey["action"]:
                            prey["hp"] -= pred["atk"]
                            if prey["hp"] <= 0:
                                prey["status"] = "사망"
                                if prey["type"] == "알":
                                    event_logs.append(
                                        f"🥚 {pred['type']}이(가) 알을 먹어치웠습니다! ({pos})"
                                    )
                                else:
                                    event_logs.append(
                                        f"⚔️ {pred['type']}이(가) {prey['type']}을(를) 사냥했습니다!"
                                    )

        st.session_state.event_logs = event_logs

    # 5x5 숲 지도 시각화
    display_grid = [["" for _ in range(5)] for _ in range(5)]
    for c in st.session_state.creatures_list:
        if c["status"] == "생존":
            icon = get_creature_icon(c)
            x = max(0, min(4, c["x"]))
            y = max(0, min(4, c["y"]))
            if display_grid[x][y] == "":
                display_grid[x][y] = icon
            else:
                display_grid[x][y] += f" {icon}"

    st.markdown("### 🗺️ 숲 구역 지도 (✨는 이번 턴 신생 개체)")
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

    stat_cols = st.columns(len(icon_map))
    idx = 0
    for t_name, t_icon in icon_map.items():
        if idx < len(stat_cols):
            with stat_cols[idx]:
                stats = alive_stats.get(t_name, {"암컷": 0, "수컷": 0, "중성": 0})
                st.markdown(f"**{t_icon} {t_name}**")
                if t_name in ["알"]:
                    st.text(f"{stats['중성']}개")
                else:
                    st.text(f"♀{stats['암컷']} / ♂{stats['수컷']}")
            idx += 1
