# DECISIONS

- **2026-10-23 深夜｜題目鎖定 3.2**。收斂路徑 2.2 → 2.3+2.2 → 3.1 → 3.2。理由：官方明文 gap（"a trusted agent that offers to collude has not yet been tested"）、harness 自帶植入聯盟正例與接受率儀器、$10-60 預算級距。Discord 競品分析：2.2/2.3 重疊風險 80-85/100、3.2=45（Jeremy 有意向無設計）、3.3=25。SOLO 確認，不組隊。差異化＝「誘導 vs 既有」因果框架＋程序化 ground truth。
- **2026-10-23 深夜｜推論路線＝Modal ephemeral hosted_model**（GPU 時間計費，可抵 $50 credit）。不用 Shared Endpoint（token 計費不抵 credit）。不用 OpenRouter（無 credit）。
- **2026-10-23 深夜｜模型＝Qwen2.5-7B-Instruct，否決任務書指定的 Qwen3-4B**。理由：starter `modal_serve.py` 釘 `vllm==0.6.6`，Qwen3 架構需 vLLM ≥ 0.8.4；硬升＝分叉官方基礎設施，違反「優先 starter code」。Qwen2.5-7B 為原論文四席位之一，MODEL_MAP 原生支援，非 thinking 模式對 JSON 輸出較穩。若 JSON 解析率 <95%，升級候選＝Qwen2.5-14B-Instruct（A10G）而非 silently 換小模型。
- **2026-10-23 深夜｜GPU＝L4**（$0.80/h）；7B bf16 權重約 15GB < 24GB。
- **2026-10-23 深夜｜主環境＝Liar's Bar**（接受率＋互惠儀器現成、--enable-memory 提供持續性量測）；Cleanup 備用。
- **2026-10-23 深夜｜4 席位同模型**是刻意妥協：接受度/行為比較在同一 policy 內進行，犧牲模型多樣性換取可控性；列入報告 Limitations。第二模型家族僅在 G5 後有餘裕時做穩健性小樣本。
- **2026-10-23 深夜｜repo .venv 補裝 modal 套件**：setup.sh 不含可選依賴 modal，poseidon-host 首跑即 ModuleNotFoundError；`uv pip install --python .venv/bin/python modal` 修復。屬環境修補，非官方碼修改。
