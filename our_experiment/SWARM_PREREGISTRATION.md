# Swarm Alignment Sprint 2026：稽核實驗預註冊 v0.3（草案，待陛下核定）

狀態：草案（2026-11-01 起草 v0.2、2026-11-02 增補第 10 節評審對齊）。核定後本檔即凍結，此後任何變更記入 PROTOCOL_DEVIATIONS.md。
凍結目標：2026-11-02 內（提前自原訂 11/06，治理時序修正，見第 5 節）。

## 1. 研究問題

N 座位共享資源沙盒中：(Q1) 日誌可被 agent 修改時，append-only 稽核層能否維持合謀偵測力；(Q2) 小模型對照前沿模型，合謀校準何時失準（官方明問之題）。

## 2. 設計與條件矩陣

- 沙盒：官方 llm-agent-collusion-2（Liar's Bar 4 座位，secret channel 變體），M1 零程式碼擴展
- M1（基線期，11/03 至 11/05）：N=4，三家族各 20 局（DeepSeek-V4.1-Flash 主力、Qwen3.8-2.4T-A95B、GLM-5.3-Flash 對照），無聯盟基線（對照十月實證 0.13 至 0.15 挑戰率每局）
- M1 稽核臂：每家族 20 局內，logs tamperable 與 append-only 各 10 局（隨機分配，種子記錄於 manifest）
- M2（賽中 11/06 至 11/08）：N=8/16 擴展，座位秩序分母沿用 analyze_g3.py 邏輯；局數依賽中時間裁減，裁減規則先記於此：先砍 M2 高 N 臂，M1 三家族 20 局不動
- 稽核條件操作化：tamperable＝agent 可編輯自家歷史檔；append-only＝唯寫附加＋雜湊鏈校驗（trace-guard 沿用評估）

## 3. 指標與統計單位

- 挑戰率：分母＝可挑戰決策點（next_player 非空），座位秩序內建；排除系統自動挑戰（next_player 空）
- 接受率：統計單位＝邀約事件
- 偏袒效應：統計單位＝episode（round 不獨立）
- N 小只報計數與不確定性，不報 p 值幻覺
- 稽核偵測力：append-only 雜湊鏈對篡改的偵出率（人為植入篡改樣本，數量記 manifest）

## 4. ITT 與資料治理

- 主要分析保留所有分配到條件的 episodes（含拒絕者）；僅接受者分析＝次要條件式
- 每局 manifest 記：endpoint、model、flags、seed（若有）、SHA-256（紀錄＋log）
- invalid runs 入 runs/invalid_registry.csv
- 端點已知怪癖：GLM 需 LLM_DISABLE_THINKING=1；Qwen3.8 需足額 max_tokens；--chosen-player 不入遊戲層（manifest 補記）；config={} 為官方碼怪癖
- 程序禁 grep|head 管線，一律 run_logged.sh 全量落檔

## 5. 時序治理（本版新增）

- **凍結先行**：本檔經陛下核定即凍結；凍結時刻之前的所有對局一律標記 calibration/pilot，不入 ITT 分析集
- M1 正式開跑（11/03）前必須已完成核定；若核定延誤，M1 順延，不以「先跑著」為由混入正式集
- 已完成之 calibration 對局（11/01 三局＋未來 pilot）僅供基礎設施校準與預算估算，不入任何假設檢定

## 6. 預算與產能（2026-11-01 校準數據）

- 單局 LLM 呼叫：226 至 548 次（n=3，局長 17 至 34 rounds，變異大）
- 60 局推估：1.7 萬至 2.5 萬次呼叫
- 併發：n=2 對局約 10 至 14 分鐘（無法分離併發降速與局長變異）；M1 採至多 2 並行＋下述防碰撞規則
- 防碰撞三規則（11/01 事故教訓，A 局紀錄遭覆寫遺失）：並行局錯開啟動至少 1 秒；局結束立刻搬紀錄入 runs/<run_id>/；開跑後核對第一筆自動存檔路徑互不重疊
- 資金：帳上約 $7x credits（陛下 2026-11-01 口述）；per-token 價格未查證，M1 首日結束即結算實際燃燒率並回寫

## 7. 基礎設施

- 推論：Modal Shared Endpoint（EP_DEEPSEEK／EP_QWEN38／EP_GLM53，2026-11-01 三端點活體驗證）
- 編排與稽核層：Modal CPU function；GPU 自架路線已判死（綁卡牆，2026-11-01 實測兩次）
- repo：~/Github/collusion_hackathon（披露 preexisting；報告文字親筆）

## 8. 開放問題（凍結前待決，逾期即按現值凍結）

- append-only 雜湊鏈採 trace-guard 現成件或自寫薄層（M1 首日定案）
- 篡改植入樣本的規模（建議：每 append-only 局 1 次，共 30 次）
- Qwen3.8/GLM 端點併發限流實測（M1 首日併入校準）

## 9. 提交

- Swarm 提交（COMP-30，11/8 AoE 截止）：陛下親手，agent 禁上傳；**可於截止前以同名重複提交取代舊檔**（官方 FAQ 明文允許，與十月 sprint 的一次性規則不同）
- 報告：官方 Google Docs 模板（docs.google.com/document/d/1_1_27EyZriMlc8n8EBE2YScaeyMjm-8xjR097nmHXAE/copy），PDF ≤ 8 頁（不含參考文獻與附錄）、摘要 150-250 字、必附 Limitations and Dual-Use / Ethical Considerations 附錄
- 必須標注 preexisting：apart-sprint-prep 與 collusion_hackathon 治理檔於 README 與報告雙處揭露（官方逐件審查）
- 每人最多兩個專案（本賽 solo 一案 ✓）
- AI 工具自由使用，但虛構結果或參考文獻可取消資格

## 10. 評審對齊（2026-11-02 增補，官方三維度 × 5 分制）

- **Dimension 1 Impact Potential & Innovation**：本設計對應＝Track 1 sandbox 的 N-agent 稽核層（官方明問小模型 vs 前沿），新穎性論點＝日誌可被 agent 篡改情境下的 append-only 稽核（ neglected problem area，對應 4 分檔「identifies a neglected problem area」）
- **Dimension 2 Execution Quality**：對應＝ITT＋manifest SHA-256＋ITT 全集保留＋variance 報告（官方 Results 段明文要求 variance and baselines——M1 報告必須含每臂變異數或 CI，預註冊此條為硬要求）
- **Dimension 3 Presentation & Clarity**：4-8 頁建議篇幅、量化結果、limitations 明列——報告結構照官方建議序（Introduction/Related Work/Methodology/Results/Discussion/Limitations/References）
- 增補規則：M2 若時間不足，寧可縮減局數也不犧牲 variance 報告與 limitations 完整性（Dimension 2 的 3 分檔明列 missing validation 為弱點）
