# DECISIONS

- **2026-10-23 深夜｜題目鎖定 3.2**。收斂路徑 2.2 → 2.3+2.2 → 3.1 → 3.2。理由：官方明文 gap（"a trusted agent that offers to collude has not yet been tested"）、harness 自帶植入聯盟正例與接受率儀器、$10-60 預算級距。Discord 競品分析：2.2/2.3 重疊風險 80-85/100、3.2=45（Jeremy 有意向無設計）、3.3=25。SOLO 確認，不組隊。差異化＝「誘導 vs 既有」因果框架＋程序化 ground truth。
- **2026-10-23 深夜｜推論路線＝Modal ephemeral hosted_model**（GPU 時間計費，可抵 $50 credit）。不用 Shared Endpoint（token 計費不抵 credit）。不用 OpenRouter（無 credit）。
- **2026-10-23 深夜｜模型＝Qwen2.5-7B-Instruct，否決任務書指定的 Qwen3-4B**。理由：starter `modal_serve.py` 釘 `vllm==0.6.6`，Qwen3 架構需 vLLM ≥ 0.8.4；硬升＝分叉官方基礎設施，違反「優先 starter code」。Qwen2.5-7B 為原論文四席位之一，MODEL_MAP 原生支援，非 thinking 模式對 JSON 輸出較穩。若 JSON 解析率 <95%，升級候選＝Qwen2.5-14B-Instruct（A10G）而非 silently 換小模型。
- **2026-10-23 深夜｜GPU＝L4**（$0.80/h）；7B bf16 權重約 15GB < 24GB。
- **2026-10-23 深夜｜主環境＝Liar's Bar**（接受率＋互惠儀器現成、--enable-memory 提供持續性量測）；Cleanup 備用。
- **2026-10-23 深夜｜4 席位同模型**是刻意妥協：接受度/行為比較在同一 policy 內進行，犧牲模型多樣性換取可控性；列入報告 Limitations。第二模型家族僅在 G5 後有餘裕時做穩健性小樣本。
- **2026-10-24 凌晨｜路線改判（推翻本檔上方「ephemeral hosted_model」決策）**：L4 ephemeral GPU function 死於綁卡牆（`InvalidError: payment method required`）；正式推論路線改判 **Modal Shared Endpoint**。**計費歸因同時修正**：帳面 $80.00→$79.99 僅證明「有扣款」，Modal 文件指 Plan Credits 不適用 Shared Endpoints——歸屬未證實前所有成本記「estimated, attribution unverified」（B4 跟蹤，usage/billing 頁核實）。
- **2026-10-24 凌晨｜模型改判（推翻「Qwen2.5-7B-Instruct 主模型」）**：主模型＝DeepSeek-V4.1-Flash（Shared Endpoint，完整 episode 實跑成功）；Qwen3.8-2.4T-A95B＝candidate robustness model（僅煙霧通過、單價高，主實驗有效後才投入完整驗證）；Qwen2.5-7B-Instruct 降為未用備案（vllm 0.6.6 相容性結論本身仍有效）。
- **2026-10-24 凌晨｜補丁與工具記錄**：`593cba9`（LLM_DISABLE_THINKING，env 旗標式 extra_body 注入）＋`e8ac2c8`（with_endpoint.sh 家族切換器，零金鑰入檔）。
- **2026-10-24 凌晨｜L4 綁卡牆發現**：GPU function 需付款方式、Shared Endpoint 不需要；poseidon-host 路線留備援（日後啟用需陛下綁卡或先解決 credit 歸屬）。
- **2026-10-24 凌晨｜端點凍結令**：DeepSeek＋Qwen3.8 入選；Kimi-K3 淘汰（`reasoning_effort=none` 被端點無視）；Inkling-NVFP4／GLM-5.3-Flash 凍結不測；ZAI 免費層降級為單呼叫 pilot 專用（25 分鐘跑不完一局，bg_87 實證）。
- **2026-10-24 凌晨｜Phase 0 審核結案**：ChatGPT 獨立審核判 Conditional GO——工程管線 PASS、科學有效性 Pending G3、成本歸因待核實。裁定：G3 通過前不得跑正式 C0-C4。
- **2026-10-24 凌晨｜端點凍結令解除（陛下指示）**：Kimi／Inkling／GLM-5.3-Flash 完成煙霧歸檔。結果：Inkling 經 `LLM_REASONING_EFFORT=none` 補丁後可用（第三家族備位）；Kimi 與 GLM-5.3-Flash 思考不可壓制、維持不可用。**研究模型裁定不變**：主 DeepSeek、candidate Qwen3.8；新端點僅入庫存，入研究須過閘（主實驗有效＋單價核實）。
