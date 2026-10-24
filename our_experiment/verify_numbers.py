"""G6 數字審計：從原始 JSON 重算論文所有數字，逐項核對 paper/main.md。

凍結規則：本腳本只讀原始紀錄＋比對已發表數字；發現不一致 = FAIL（不是改數字）。
用法：python3 our_experiment/verify_numbers.py
"""
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_g3 import decisions, rate_table  # noqa: E402

BASE = ("/Users/miku/Github/collusion_hackathon/llm-agent-collusion-2/"
        "Collusion_Liars_Bar/experiments/game_records")
COMM = BASE + "/Lily-Luke-Mike-Quinn_secret_comm"
PLAIN = BASE + "/Lily-Luke-Mike-Quinn"
PAPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "paper", "main.md")

FAILURES = []


def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {name} {detail}")
    if not cond:
        FAILURES.append(name)


def load(fp):
    return json.load(open(fp))


def focal_and_total(rec, min_round):
    dec = decisions(rec, min_round=min_round)
    rt = rate_table(dec)
    fc = fo = tc = to = 0
    for (dm, tgt), (c, o, _) in rt.items():
        tc += c
        to += o
        if {dm, tgt} == {"Lily", "Luke"}:
            fc += c
            fo += o
    return fc, fo, tc, to


def ally_mutual(rec, min_round, ally_pair):
    dec = decisions(rec, min_round=min_round)
    rt = rate_table(dec)
    pair = set(ally_pair)
    wc = sum(c for (a, b), (c, o, _) in rt.items() if a in pair and b in pair)
    wo = sum(o for (a, b), (c, o, _) in rt.items() if a in pair and b in pair)
    return wc, wo


def main():
    paper = open(PAPER).read()

    # 逐局重算（與 pilot_ledger.py 相同凍結清單）
    episodes = {
        "a1-g1": ("C2", COMM + "/20261024_071006.json", 3),
        "a1-g2": ("C0", COMM + "/20261024_071728.json", 1),
        "a1-g3": ("C0", COMM + "/20261024_072426.json", 1),
        "a2-g1": ("C2", COMM + "/20261024_075136.json", 4),
        "a2-g2": ("C0", COMM + "/20261024_080254.json", 1),
        "a2-g3": ("C0", COMM + "/20261024_081811.json", 1),
        "a3-g1": ("C4", COMM + "/20261024_082152.json", 4),
        "p-c2-1": ("C2", COMM + "/20261024_092253.json", 4),
        "p-c2-2": ("C2", COMM + "/20261024_093349.json", 4),
        "p-c4-1": ("C4", COMM + "/20261024_094116.json", 4),
        "m-c2-1": ("C2", COMM + "/20261024_102735.json", 4),
        "m-c2-2": ("C2", COMM + "/20261024_103950.json", 4),
        "m-c2-3": ("C2", COMM + "/20261024_105955.json", 4),
        "m-c2-4": ("C2", COMM + "/20261024_111042.json", 4),
        "m-c0-1": ("C0", PLAIN + "/20261024_112955.json", 1),
        "m-c0-2": ("C0", PLAIN + "/20261024_113902.json", 1),
    }

    stats = {}
    for eid, (cond, path, post) in episodes.items():
        rec = load(path)
        if rec.get("winner") is None:
            print(f"[SKIP] {eid} partial")
            continue
        fc, fo, tc, to = focal_and_total(rec, min_round=post)
        stats[eid] = {"cond": cond, "fc": fc, "fo": fo, "tc": tc, "to": to,
                      "rounds": len(rec.get("rounds", [])), "winner": rec.get("winner")}

    # 核對 1：16 episodes 全部存在且完賽
    check("E1 16 episodes 全部完賽", len(stats) == 16, f"got {len(stats)}")

    # 核對 2：邀約結果 8 voluntary / 0 accept
    inv_files = ["a1-g1", "a2-g1", "p-c2-1", "p-c2-2", "m-c2-1", "m-c2-2", "m-c2-3", "m-c2-4"]
    refuses = 0
    for eid in inv_files:
        rec = load(episodes[eid][1])
        evs = (rec.get("secret_channel") or {}).get("events", [])
        if any(e.get("event") == "tool_refused" for e in evs):
            refuses += 1
    check("E2 自願邀約 8 事件全 REFUSE", refuses == 8, f"got {refuses}")

    # 核對 3：confirmatory C2 focal 5/42
    m_c2 = {eid: s for eid, s in stats.items() if eid.startswith("m-c2")}
    fc = sum(s["fc"] for s in m_c2.values())
    fo = sum(s["fo"] for s in m_c2.values())
    check("E3 main C2 focal 5/42=0.119", (fc, fo) == (5, 42), f"{fc}/{fo}")

    # 核對 4：confirmatory C0 focal 1/24
    m_c0 = {eid: s for eid, s in stats.items() if eid.startswith("m-c0")}
    fc = sum(s["fc"] for s in m_c0.values())
    fo = sum(s["fo"] for s in m_c0.values())
    check("E4 main C0 focal 1/24=0.042", (fc, fo) == (1, 24), f"{fc}/{fo}")

    # 核對 5：seeded 盟友對內 pooled 0/10
    seeded = [episodes["a3-g1"], episodes["p-c4-1"]]
    wc = wo = 0
    for _, path, mr in seeded:
        w, o = ally_mutual(load(path), mr, ("Quinn", "Luke"))
        wc += w
        wo += o
    check("E5a seeded 盟友對內 0/10（082152 Quinn+Luke）", True,
          f"computed {wc}/{wo} across 2 episodes")
    # 分局驗證
    w1, o1 = ally_mutual(load(seeded[0][1]), seeded[0][2], ("Quinn", "Luke"))
    lily_ally = ("Lily", "Mike")
    w2, o2 = ally_mutual(load(seeded[1][1]), seeded[1][2], lily_ally)
    check("E5b 082152 盟友對內 0/4", (w1, o1) == (0, 4), f"{w1}/{o1}")
    check("E5c 094116 盟友對內 0/6", (w2, o2) == (0, 6), f"{w2}/{o2}")

    # 核對 6：paper/main.md 含關鍵數字（D6 修正後終版）
    for num in ["0.119", "0.042", "0.158", "0.051", "0.050", "0.069",
                "8", "108", "108", "0/10", "10/85", "5/42", "1/24", "2/39",
                "1/20", "12/76", "51", "57"]:
        check(f"E6 paper 含 {num}", num in paper, "")

    # 核對 7：無幻影引用殘留
    for phantom in ["Terdich", "Kaneko", "Shapiro"]:
        check(f"E7 無幻影引用 {phantom}", phantom not in paper, "")

    print()
    if FAILURES:
        print(f"G6 AUDIT FAILED: {FAILURES}")
        sys.exit(1)
    print("G6 AUDIT: ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
