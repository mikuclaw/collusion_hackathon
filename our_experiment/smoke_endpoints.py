"""多端點煙霧器：每端點跑 default 與 reasoning_effort=none 各一呼叫（max_tokens=256＝遊戲上限）。

判定：content 非空且可解析 JSON＝可用；reasoning 吃滿額度＝此端點需 client 端抑制
（官方 llm_client 送不出該欄位＝不可用，除非打補丁）。
金鑰從 repo-root compute.env 讀（MODAL_PROXY_TOKEN_ID.SECRET），本檔不含 secret。
用法：python3 our_experiment/smoke_endpoints.py [name ...]  # 不帶參數＝全部
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
env = {}
for line in (REPO / "compute.env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
KEY = f"{env['MODAL_PROXY_TOKEN_ID']}.{env['MODAL_PROXY_TOKEN_SECRET']}"

PROMPT = ("You are Lily in Liar's Bar. Reply ONLY with strict JSON: "
          '{"played_cards": [1], "behavior": "aggressive", "play_reason": "five words max"}')

TARGETS = {
    "deepseek": (env["EP_DEEPSEEK"], env["MODEL_DEEPSEEK"]),
    "qwen38":   (env["EP_QWEN38"],   env["MODEL_QWEN38"]),
    "kimi":     (env["EP_KIMI_K3"],  env["MODEL_KIMI_K3"]),
    "inkling":  (env["EP_INKLING"],  env["MODEL_INKLING"]),
    "glm53":    (env["EP_GLM53"],    env["MODEL_GLM53"]),
}


def call(url: str, model: str, extra: dict) -> bool:
    body = {"model": model,
            "messages": [{"role": "user", "content": PROMPT}],
            "max_tokens": 256, "temperature": 0.8, "top_p": 0.95, **extra}
    req = urllib.request.Request(
        url.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.loads(r.read())
    dt = time.time() - t0
    ch = d["choices"][0]
    m = ch["message"]
    c = m.get("content") or ""
    rc = m.get("reasoning_content") or ""
    try:
        json.loads(c)
        ok = len(c) > 0
    except Exception:
        ok = False
    print(f"  {dt:5.2f}s content={len(c):4d}c reasoning={len(rc):5d}c "
          f"finish={ch.get('finish_reason')} usage={d.get('usage', {}).get('total_tokens')} "
          f"{'USABLE' if ok else 'UNUSABLE'}")
    return ok


only = set(sys.argv[1:])
for name, (url, model) in TARGETS.items():
    if only and name not in only:
        continue
    print(f"=== {name} ({model}) ===")
    try:
        call(url, model, {})
    except Exception as e:
        print(f"  default failed: {str(e)[:140]}")
    try:
        call(url, model, {"reasoning_effort": "none"})
    except Exception as e:
        print(f"  reasoning_effort=none rejected: {str(e)[:140]}")
