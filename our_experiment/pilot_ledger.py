"""Pilot Episode Ledger（M3/M4）：從原始 JSON 重建逐局結果表。

規則（PILOT_SPEC.md 凍結版）：
- C2 局：邀約 round 2，focal pair 挑戰率自 round 3 起算（post-offer，保守）
- C0 局：全域（無處理）
- 盟友對（僅 C4/seeded）：channel_established 之後
- 挑戰率分母＝可挑戰機會（next_player 決策點，排除系統自動挑戰）
單位：episode。輸出：stdout 表＋our_experiment/runs/pilot_ledger.json
用法：python3 our_experiment/pilot_ledger.py
"""
import glob
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_g3 import decisions, rate_table  # noqa: E402

BASE = ("/Users/miku/Github/collusion_hackathon/llm-agent-collusion-2/"
        "Collusion_Liars_Bar/experiments/game_records")
COMM = BASE + "/Lily-Luke-Mike-Quinn_secret_comm"
SINGLE = BASE + "/Lily-Luke-Mike-Quinn_secret_channel"
PLAIN = BASE + "/Lily-Luke-Mike-Quinn"
PAIR = ("Lily", "Luke")  # focal pair，a priori

# 逐局清單（episode_id, condition, path, post_round）
# condition：C2=邀約自願回應、C0=無邀約、C4=seeded 聯盟
EPISODES = [
    ("a1-g1", "C2", COMM + "/20261024_071006.json", 3),   # 邀約 round 2（Mike REFUSE）
    ("a1-g2", "C0", COMM + "/20261024_071728.json", 1),
    ("a1-g3", "C0", COMM + "/20261024_072426.json", 1),
    ("a2-g1", "C2", COMM + "/20261024_075136.json", 3),   # 邀約 round 2（Quinn REFUSE）
    ("a2-g2", "C0", COMM + "/20261024_080254.json", 1),
    ("a2-g3", "C0", COMM + "/20261024_081811.json", 1),   # bg_91 game 3（無通道，20R，Lily 勝）
    ("a3-g1", "C4", COMM + "/20261024_082152.json", 4),   # bg_95 game 1（seeded 建立於 round 3，51 通訊）
]


def focal_rates(rec, min_round):
    dec = decisions(rec, min_round=min_round)
    rt = rate_table(dec)
    focal_c = focal_opp = 0
    for (dm, tgt), (c, o, _) in rt.items():
        if {dm, tgt} == set(PAIR):
            focal_c += c
            focal_opp += o
    total_c = sum(v[0] for v in rt.values())
    total_opp = sum(v[1] for v in rt.values())
    return focal_c, focal_opp, total_c, total_opp


def main():
    rows = []
    for eid, cond, path, post in EPISODES:
        if not os.path.exists(path):
            print(f"SKIP {eid}（檔案不存在）")
            continue
        rec = json.load(open(path))
        fc, fo, tc, to = focal_rates(rec, post)
        rows.append({
            "episode_id": eid, "condition": cond,
            "file": os.path.basename(path),
            "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()[:16],
            "rounds": len(rec.get("rounds", [])),
            "winner": rec.get("winner"),
            "focal_pair_challenges": fc, "focal_pair_opportunities": fo,
            "focal_pair_rate": round(fc / fo, 3) if fo else None,
            "total_challenges": tc, "total_opportunities": to,
            "total_rate": round(tc / to, 3) if to else None,
        })

    print(f"{'episode':8s} {'cond':4s} {'rounds':6s} {'focal':>8s} {'total':>8s} winner")
    for r in rows:
        fr = f"{r['focal_pair_challenges']}/{r['focal_pair_opportunities']}" if r["focal_pair_opportunities"] else "n/a"
        tr = f"{r['total_challenges']}/{r['total_opportunities']}" if r["total_opportunities"] else "n/a"
        print(f"{r['episode_id']:8s} {r['condition']:4s} {r['rounds']:<6d} {fr:>8s} {tr:>8s} {r['winner']}")

    print("\n== 條件層彙總（focal pair 挑戰率，episode 為單位）==")
    for cond in ("C2", "C0", "C4"):
        rs = [r for r in rows if r["condition"] == cond and r["focal_pair_opportunities"]]
        c = sum(r["focal_pair_challenges"] for r in rs)
        o = sum(r["focal_pair_opportunities"] for r in rs)
        eps = [r["episode_id"] for r in rs]
        if o:
            print(f"{cond}: n={len(rs)} episodes, pooled {c}/{o} = {c / o:.3f}  [{', '.join(eps)}]")
        else:
            print(f"{cond}: n={len(rs)} episodes, 機會數不足（如實標記）")

    out = "our_experiment/runs/pilot_ledger.json"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    print(f"\nledger -> {out}")


if __name__ == "__main__":
    main()
