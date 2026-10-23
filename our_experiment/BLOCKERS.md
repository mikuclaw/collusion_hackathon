# BLOCKERS

- **B1（使用者動作，可選）**：Discord/Slack/Luma 順手拿 Nebius 或 OpenRouter key——可完全繞過 Modal 計費歸屬問題；拿不到也不阻塞（Shared Endpoint 路線已通）。
- **B2（歸檔）**：ZAI glm-4.5-flash 免費層降級為單呼叫 pilot 專用（25 分鐘跑不完一局，bg_87 實證）；正式呼叫全走 Shared Endpoint。
- **B3（已修，記錄在案）**：官方 `modal_serve.py` 的 secret 略過邏輯在新 SDK 失效（from_name 惰性）——已用 secret 建立繞過，未動官方碼。
- **B4（審核新增，跟蹤中）**：**Shared Endpoint 計費歸屬未證實**——帳面有扣款（$80.00→$79.99）但 Modal 文件指 Plan Credits 不適用 Shared Endpoints。行動：陛下在 modal.com usage/billing 頁核對今日消耗的歸屬類別；證實前所有成本記 estimated。
- **B5（賽後）**：proxy token 已入對話紀錄，sprint 結束後於 workspace settings 輪換。
- 無其他阻塞。
