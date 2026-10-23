# EXPERIMENT_LOG

## Phase 0 preflight（2026-10-23 深夜）

| 項目 | 結果 |
|---|---|
| git clone starter repo | ✓ 7,935 files |
| branch | ✓ sprint-3.2 |
| ./setup.sh llm-agent-collusion-2 llm-trust-breaking | ✓ 2 ok（uv sync 109s） |
| Modal 認證 | ✓ ~/.modal.toml、profile=calpa |
| Modal credit 餘額 | 待 dashboard 驗證（B1） |
| ZAI glm-4.5-flash 煙霧 | ✓ HTTP 200、0.53s、finish=stop（免費層，pilot 後備） |
| 儀器盤點 | ✓ offer/accept 結構化、channel 事件記錄、series flags、接受率批次測試腳本 |
| Docker | 未裝（不需要；僅 trace-guard 要） |
| G1 第一次嘗試 | ✗ `ModuleNotFoundError: No module named 'modal'`（repo venv 缺可選依賴） |
| 修復 | ✓ `uv pip install --python .venv/bin/python modal` |
| G1 重跑 | 執行中，結果待補 |

指令存記：

```bash
# G1
./.venv/bin/poseidon-host --model Qwen/Qwen2.5-7B-Instruct --gpu L4 -- \
  ./.venv/bin/python our_experiment/smoke_endpoint.py
# G2（週六）
cd llm-agent-collusion-2/Collusion_Liars_Bar && ../../.venv/bin/python src/game/game.py
```
