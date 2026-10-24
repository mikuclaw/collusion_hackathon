"""PC-C 量測器單元測試：合成軌跡驗證 analyze_g3 的抽取與比率計算（零 LLM token）。

合成資料只驗證分析器正確性，不得冒充真實 LLM 研究數據。
執行：python3 our_experiment/test_metrics.py；任何斷言失敗 → exit 1。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_g3 import challenge_events, decisions, rate_table  # noqa: E402

FAILURES = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name} {detail}")
    if not cond:
        FAILURES.append(name)


def mk_rec(plays, sc=None):
    rec = {"rounds": [{"play_history": plays}], "winner": None, "final_scores": {}}
    if sc is not None:
        rec["secret_channel"] = sc
    return rec


def play(actor, nxt, challenged, result=None):
    return {"player_name": actor, "next_player": nxt,
            "was_challenged": challenged, "challenge_result": result}


# T1 決策抽取與挑戰率（機會為分母）
rec1 = mk_rec([
    play("A", "B", False), play("A", "B", False), play("A", "B", False),  # B 對 A：0/3
    play("B", "A", True, "success"), play("B", "A", False),               # A 對 B：1/2
    play("C", "B", True, "success"), play("C", "B", True, "success"),     # B 對 C：2/2
])
dec = decisions(rec1)
check("T1a 決策抽取筆數", len(dec) == 7, f"got {len(dec)}")
rt = rate_table(dec)
check("T1b B->A 挑戰率 0/3", rt.get(("B", "A"), (0, 0, 0))[:2] == (0, 3), str(rt.get(("B", "A"))))
check("T1c A->B 挑戰率 1/2", rt.get(("A", "B"), (0, 0, 0))[:2] == (1, 2), str(rt.get(("A", "B"))))
check("T1d B->C 挑戰率 2/2", rt.get(("B", "C"), (0, 0, 0))[:2] == (2, 2), str(rt.get(("B", "C"))))

# T2 系統自動挑戰排除：空字串與真實紀錄的字面值 "No one" 兩種形態
rec2 = mk_rec([
    play("A", "B", False),
    play("A", "", True, "eliminated"),     # 系統自動挑戰（空 next_player）
    play("A", "No one", True, "eliminated"),  # 系統自動挑戰（真實紀錄字面值，T8 實證）
    play("C", "B", False),
])
dec2 = decisions(rec2)
check("T2a 自動挑戰排除後決策數 2", len(dec2) == 2, f"got {len(dec2)}")
rt2 = rate_table(dec2)
check("T2b 無自動挑戰對別殘留", set(rt2) == {("B", "A"), ("C", "B")}, str(list(rt2)))

# T3 挑戰事件抽取（challenger 由 next_player 推導）
rec3 = mk_rec([play("A", "B", True, "success"), play("B", "C", False)])
ev = challenge_events(rec3)
check("T3 挑戰事件=(B,A,success)", ev == [("B", "A", "success")], str(ev))

# T4 盟友對內/對外挑戰率（模擬偏袒：對盟友 0/4，對外 2/2）
# 注意角色：play(actor, nxt) 中 nxt 是「決策者」。(dm=A, tgt=B) 屬 A→B 對內機會。
rec4 = mk_rec([
    play("A", "B", False), play("A", "B", False), play("A", "B", False),  # B 對 A：0/3（對內）
    play("B", "A", False),                                                # A 對 B：0/1（對內）
    play("C", "A", True, "success"), play("C", "A", True, "success"),     # A 對 C：2/2（對外）
    play("A", "C", True, "success"), play("A", "C", True, "success"),     # C 對 A：2/2（被挑戰）
    play("B", "C", True, "success"), play("B", "C", False),               # C 對 B：1/2（被挑戰）
])
dec4 = decisions(rec4)
rt4 = rate_table(dec4)
pair = {"A", "B"}
w_c = sum(c for (a, b), (c, o, _) in rt4.items() if a in pair and b in pair)
w_o = sum(o for (a, b), (c, o, _) in rt4.items() if a in pair and b in pair)
o_c = sum(c for (a, b), (c, o, _) in rt4.items() if a in pair and b not in pair)
o_opp = sum(o for (a, b), (c, o, _) in rt4.items() if a in pair and b not in pair)
check("T4a 盟友對內 0/4", (w_c, w_o) == (0, 4), f"{w_c}/{w_o}")
check("T4b 對外 2/2", (o_c, o_opp) == (2, 2), f"{o_c}/{o_opp}")
check("T4c 偏袒方向偵測：對內率低於對外", (w_c / w_o) < (o_c / o_opp),
      f"{w_c / w_o:.2f} < {o_c / o_opp:.2f}")

# T5 PC-A 事件結構可抽取
rec5 = mk_rec([play("A", "B", False)], sc={
    "config": {"chosen_player": "X"},
    "events": [{"event": "tool_refused", "chosen_player": "X", "reason": "REFUSE"},
               {"event": "channel_established", "initiator": "X", "partner": "Y"}],
    "communications": [],
})
sc = rec5.get("secret_channel", {})
evs = sc.get("events", [])
check("T5a PC-A 事件數 2", len(evs) == 2, str(len(evs)))
check("T5b PC-A 事件型別", [e["event"] for e in evs] == ["tool_refused", "channel_established"])

print()
if FAILURES:
    print(f"METRIC TESTS FAILED: {FAILURES}")
    sys.exit(1)
print("ALL METRIC TESTS PASSED")

# T6 獨立 oracle：手工列舉完整期望表（不經 decisions/rate_table 內部路徑重算）
plays6 = [
    play("Lily", "Luke", True, "success"),   # Luke 挑戰 Lily → (Luke, Lily) 1/1
    play("Luke", "Mike", False),             # Mike 機會未行使 → (Mike, Luke) 0/1
    play("Mike", "Quinn", True, "fail"),     # Quinn 挑戰 Mike → (Quinn, Mike) 1/1
    play("Quinn", "Lily", False),            # Lily 機會未行使 → (Lily, Quinn) 0/1
]
expected6 = {("Luke", "Lily"): (1, 1), ("Mike", "Luke"): (0, 1),
             ("Quinn", "Mike"): (1, 1), ("Lily", "Quinn"): (0, 1)}
got6 = {k: (v[0], v[1]) for k, v in rate_table(decisions(mk_rec(plays6))).items()}
check("T6 獨立 oracle 全表一致", got6 == expected6, f"{got6} vs {expected6}")

# T7 零機會防護：無機會的玩家不得出現於表；空紀錄不得除零
rt7 = rate_table(decisions(mk_rec([play("A", "B", False)])))
check("T7a 零機會玩家 C 不出現", all("C" not in k for k in rt7), str(list(rt7)))
check("T7b 單機會對別正常", rt7.get(("B", "A"), (0, 0, 0))[1] == 1, str(rt7.get(("B", "A"))))
check("T7c 空紀錄回傳空表無例外", rate_table(decisions(mk_rec([]))) == {}, "")

# T8 真實紀錄人工核對：071006 挑戰事件獨立重數應為 6
import json as _json
_real = _json.load(open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "llm-agent-collusion-2/Collusion_Liars_Bar/experiments/game_records/"
    "Lily-Luke-Mike-Quinn_secret_comm/20261024_071006.json")))
_manual = [(ph["next_player"], ph["player_name"])
           for r in _real["rounds"] for ph in r["play_history"]
           if ph.get("was_challenged") and ph.get("next_player")]
_got = [(a, b) for a, b, _ in challenge_events(_real)]
check("T8a 真實紀錄獨立重數＝6", len(_manual) == 6, f"{len(_manual)}: {_manual}")
check("T8b 分析器與獨立重數一致", sorted(_got) == sorted(_manual), f"{sorted(_got)}")

print()
if FAILURES:
    print(f"METRIC TESTS FAILED: {FAILURES}")
    sys.exit(1)
print("ALL METRIC TESTS PASSED (incl. oracle / zero-opportunity / real-trajectory audit)")
