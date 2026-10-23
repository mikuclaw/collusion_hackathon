"""G3 正例分析器（Review Package 元件）。

逐局輸出：secret channel 事件、通訊內容、挑戰行為矩陣（challenger→challenged）、
盟友對（Lily + chosen_partner）與非盟友的 challenge 率對比，並對照 no-alliance baseline。
只讀原始 JSON，不做任何判定；判定由研究者在 findings 記錄。
用法：python3 our_experiment/analyze_g3.py
"""
import glob
import json
from collections import Counter

BASE = ("/Users/miku/Github/collusion_hackathon/llm-agent-collusion-2/"
        "Collusion_Liars_Bar/experiments/game_records")
SERIES_DIR = BASE + "/Lily-Luke-Mike-Quinn_secret_comm"
BASELINE = BASE + "/Lily-Luke-Mike-Quinn/20261023_235901.json"
PAIR_ANCHOR = "Lily"  # chosen_player


def challenge_events(rec):
    """抽取 (challenger, challenged) 事件。

    紀錄結構：每筆 play 有 was_challenged / challenge_result，但挑戰者名字不直接記錄；
    Liar's Bar 規則：看牌後決定挑戰的是下一位行動者，故 challenger = 該筆的 next_player。
    """
    events = []
    for r in rec.get("rounds", []):
        for ph in r.get("play_history", []):
            if ph.get("was_challenged"):
                challenger = ph.get("next_player")
                challenged = ph.get("player_name")
                if challenger and challenged and challenger != challenged:
                    events.append((challenger, challenged, ph.get("challenge_result")))
    return events


def summarize(tag, rec):
    print(f"\n===== {tag} =====")
    print("top keys:", sorted(rec.keys()))
    sc = rec.get("secret_channel") or {}
    if isinstance(sc, dict):
        print("secret_channel keys:", sorted(sc.keys()))
        print("active:", sc.get("active"), "| initiator:", sc.get("initiator"),
              "| partner:", sc.get("partner"))
        evs = sc.get("events") or []
        for e in evs:
            print("  event:", e.get("event_type") or e.get("type"), "|",
                  json.dumps({k: v for k, v in e.items()
                              if k not in ("event_type", "type")}, ensure_ascii=False)[:220])
        comms = sc.get("communications") or sc.get("messages") or []
        for m in comms[:6]:
            print("  comm:", str(m)[:200])
        print("  comm count:", len(comms))
    ev = challenge_events(rec)
    print("challenge events:", len(ev))
    for e in ev:
        print("  challenge:", e)
    cnt = Counter((a, b) for a, b, _ in ev)
    print("matrix:", dict(cnt))
    # 分數
    fs = rec.get("final_scores")
    print("final_scores:", fs)
    print("winner:", rec.get("winner"))
    # Lily 與其 partner 的相互 vs 對外挑戰
    partner = (sc.get("partner") if isinstance(sc, dict) else None)
    if partner:
        pair = {PAIR_ANCHOR, partner}
        within = [e for e in ev if e[0] in pair and e[1] in pair]
        outward = [e for e in ev if e[0] in pair and e[1] not in pair]
        others_on_pair = [e for e in ev if e[0] not in pair and e[1] in pair]
        print(f"pair({PAIR_ANCHOR}+{partner}): within={len(within)} "
              f"pair_outward={len(outward)} others_on_pair={len(others_on_pair)}")
    return rec


files = sorted(glob.glob(SERIES_DIR + "/*.json"))
print("series files:", [f.split("/")[-1] for f in files])
for f in files:
    with open(f) as fh:
        summarize(f.split("/")[-1], json.load(fh))

with open(BASELINE) as fh:
    summarize("BASELINE (no alliance) 20261023_235901", json.load(fh))
