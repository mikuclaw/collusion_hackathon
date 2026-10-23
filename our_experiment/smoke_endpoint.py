"""Phase 0 smoke test: ephemeral Modal vLLM endpoint, two timed calls.

在 poseidon-host 包裹下執行；hosted_model 會把 llm_config 指向暫時端點。
驗收：CALL1 純文字回應非空；CALL2 嚴格 JSON 可解析（解析率是我們遊戲 harness 的命脈）。
"""
import json
import time

from poseidon_compute import make_client

MODEL = "Qwen/Qwen2.5-7B-Instruct"
client = make_client()

# CALL 1: plain completion
t0 = time.time()
r1 = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "Reply with exactly: READY"}],
    max_tokens=8,
    temperature=0,
)
dt1 = time.time() - t0
txt1 = r1.choices[0].message.content or ""
print(f"CALL1 plain {dt1:.2f}s len={len(txt1)} usage={r1.usage.total_tokens} text={txt1[:40]!r}")

# CALL 2: strict JSON (game harness 需要的輸出形狀)
t0 = time.time()
r2 = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": 'Return STRICT JSON only, no markdown fences: {"accept": true, "reason": "five word reason"}',
        }
    ],
    max_tokens=64,
    temperature=0,
)
dt2 = time.time() - t0
raw2 = r2.choices[0].message.content or ""
try:
    json.loads(raw2)
    ok = True
except Exception:
    ok = False
print(f"CALL2 json {dt2:.2f}s parse_ok={ok} usage={r2.usage.total_tokens} raw={raw2[:80]!r}")

print("SMOKE_PASS" if (txt1 and ok) else "SMOKE_FAIL")
