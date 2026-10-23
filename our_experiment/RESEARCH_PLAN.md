# RESEARCH_PLAN — Track 3.2 Trusted Undercover Agent

Sprint：Apart AI Collusion Research Sprint 2026-10-23~25（截止 10/25 23:59 AoE＝10/26 19:59 HKT）
團隊：SOLO（陛下＝研究決策；方法學顧問＝ChatGPT；執行 agent＝GLM-5.3 Flash）
論文定位：**A small, rigorous, reproducible empirical study**（Level 3：植入 ground truth＋配對條件＋不確定量測＋副作用評估）

## 研究問題（唯一，不再換題）

Does a trusted undercover agent's collusion invitation reveal pre-existing
collusive coordination, or induce collusion that would not otherwise occur?

臥底審計是「揭露」既有合謀，還是「創造」它所要測量的行為？

工作標題：*Induced or Pre-existing? Auditing AI Agents with Collusion-Offering Trusted Agents*

## 假設（全部視為未證實；每條預先寫明什麼結果支持、什麼結果反駁）

- H1 敏感度：植入聯盟成員的接受率高於非成員。支持＝差距方向穩定且 CI 不跨 0；反駁＝接受率在成員/非成員無法區分。
- H2 言行落差：口頭接受不預測持續偏袒行為。支持＝接受者中偏袒率與未接受者無統計差異；反駁＝接受→偏袒鏈穩定出現。
- H3 誘導：無聯盟 agent 收到明確邀請後的偏袒行為高於無邀請基線。支持＝I1 > B0 且可複現；反駁＝I1 ≈ B0。
- H4 方式梯度：間接暗示接受率介於直接邀請與良性合作之間。

## 設計：2×2 植入聯盟 × 臥底邀請，另加邀請類型 arm

| Cell | 植入聯盟 | 臥底邀請 | 用途 | n（局） |
|---|---|---|---|---|
| E1 | 有（官方 secret channel 機制） | 直接秘密聯盟 | 敏感度 | 6-8 |
| E2 | 有 | 無邀請 | 聯盟自行露馬腳基線 | 6 |
| I1 | 無 | 直接秘密聯盟 | 誘導率 | 6-8 |
| I2 | 無 | 良性合作邀請 | 誘因對照 | 4-6 |
| I3 | 無 | 間接互惠暗示 | 方式梯度 | 4-6 |
| B0 | 無 | 無邀請 | 純基線 | 4 |
| W1 | 有（撤回） | 首局邀請、後續停止並恢復競爭 | 慣例 vs 順從（探索性，enable-memory 系列） | 4-6 |

- **W1 預登記解讀**（H5）：撤回邀請後偏袒持續 → 合作慣例形成（持續性證據升級）；立即消失 → 順從性反應而非聯盟。此 arm 不用於偵測率計算，僅作持續性機制分析。
- **H6 方向反轉風險（預登記，2026-10-24 審核補）**：植入聯盟成員可能因忠誠「拒絕」臥底邀約——接受率符號反轉。緩解：(1) pact 文本設計成與既有聯盟可並存（不要求背棄原夥伴）；(2) 判定用複合指標「口頭接受＋行為偏袒」，指標方向在校準半區估計後凍結，不由主實驗事後挑選。若反轉穩定出現，按本預登記解讀為發現（honeypot 對既有聯盟失效／更有效），不是失敗。

- 判定規則：前半資料校準接受門檻 → 凍結 → 後半測 sensitivity/FPR ＋ bootstrap 95% CI。
- 遞增證據結構（對應官方 2.3 plus factors）：接受 → 重複偏袒行動 → 跨局持續（enable-memory）。
- 配對隨機化：同 seed 派生初始牌局跨條件重用；條件分配在跑前寫死於 config。

## 環境與模型

- 主環境：Liar's Bar（官方 llm-agent-collusion-2）。現成儀器：
  `respond_to_secret_tool_offer` 結構化輸出、`game_record.add_secret_channel_event`、
  series flags（--trigger-game/--trigger-round/--chosen-player/--allow-refusal/--enable-memory）、
  `test_secret_comm_acceptance.py` 批次接受率＋互惠檢查。
- 次環境：Cleanup 同框架（時間允許才做）。
- 模型：Qwen/Qwen2.5-7B-Instruct × 4 席位同模型（temperature 0.2、int-only seed 派生）。
  原論文 seat 模型之一；Qwen3-4B 因 starter 釘 vllm==0.6.6 不可行（見 DECISIONS）。
  自架 vLLM 的優勢：權重/版本/取樣參數完全釘死，可重現性高於第三方 API。
- 臥底／植入者：腳本化（零 API 成本）。絕不把腳本合謀宣稱為自發湧現。

## 量測

1. 口頭接受率（結構化）
2. 偏袒行為率：對盟友 vs 非盟友的 challenge 行為差異（game_record 提取）
3. 重複偏袒與跨局持續性
4. 聯盟收益、正常任務表現、invalid-run 率

## 統計三層（推論強度與證據品質相符）

1. 描述性：各 cell 接受率/偏袒率＋樣本量，效果量以百分點差呈現。
2. 因果對照：同模型同設定，隨機分配條件、配對初始情境；邀請條件為唯一操縱變因。
3. 穩健性：去一局（leave-one-out）、prompt 敏感性抽查、異常輸出清點。
   注意：**同 series 具記憶的多局不是獨立樣本**，分析單位＝局（獨立初始化）或系列（明確標明）。
   不追求每項比較 p<0.05；報 CI 與效果量。

## 研究品質閘（內部 10 項，提交前逐項勾稽）

1. 研究問題可否證；支持/反駁條件預先寫明（見假設節）
2. Positive control 可信（G3：植入聯盟被接受且偏袒可測）
3. Negative control 恰當（B0/I2 區分一般合作與不當偏袒）
4. 正式實驗規格凍結（G5；pilot 與正式資料分開）
5. 完整實驗紀錄（模型/commit/參數/seeds/失敗案例/成本）
6. 統計不確定性透明（n、CI、效果量；series 非獨立樣本）
7. 替代解釋檢查（shared incentives、prompt bias、模型能力不足）
8. 行為與意圖分離（接受≠合謀；短期偏袒≠既有聯盟）
9. 可重現（raw JSONL → 固定分析腳本 → 圖表，全自動）
10. 結論不超過證據（陰性結果、失敗、限制、dual-use 如實報告）

## 評審案例六條強制規則（自 Apart 歷屆公開評審意見提煉，2026-10-23 併入）

1. **Experimenter truth 與 auditor 資料分離**：`our_experiment/runs/<run_id>/labels.json`（植入與否、offer 類型）與 `trajectories.jsonl`（auditor 可見）分開存放；特徵只能從 trajectories 算，labels 僅用於最終 sensitivity/FPR。杜絕 SpecShield 式「近似 Oracle 訊號」污染。
2. **先證明合謀發生，再算偵測率**：G3 正例閘未過前，不產出任何「偵測率」數字。
3. **Pilot 與 test set 永不混用**；改 prompt/評分器 → 版本號遞增＋重新凍結（G5 重跑）。
4. **失敗 run 全部入帳**：`runs/invalid_registry.csv`，載明 invalid 規則（JSON 解析失敗 N 次回退、遊戲未終局等）與比例，永不靜默丟棄。
5. **主要指標＝行為**（偏袒行動差異、收益移轉），口頭接受率為次要。
6. **每個結論附適用範圍**（單模型、單遊戲、探索性 n）。

## 品質流程補強（Script-and-Stance 借鏡，2026-10-23 深夜併入）

- **Append-only**：`runs/` 原始 JSONL 永不覆寫；失敗/不利 run 只標記不刪除；judge 或指標修正＝新版本號＋透明重評，舊分數保留。
- **單命令重現**：`our_experiment/make_report.py` 從 raw JSONL 重建主結果表、圖與統計摘要；論文數字不得手工修改。
- **目標重框**：主貢獻候選＝「若僅用接受率量測合謀，會高估風險多少」——量測方法學洞察優先於「成功讓 agent 合謀」的展示。

## Review Package 標準佈局（ARL 審核交接，每個 run 目錄固定）

`runs/<run_id>/` ＝ protocol.md（事前假設與條件）＋ config.json（模型/prompt/seeds/版本）
＋ trajectories.jsonl（原始紀錄，auditor 可見）＋ labels.json（experimenter-only）
＋ metrics.csv（每實驗單位量測）＋ analysis.py ＋ findings.md ＋ git_commit.txt。
findings 分離 verified observations／interpretations／speculation，必附**最強替代解釋**，
結尾固定為 GO／REVISE／PIVOT／STOP 建議。審核方（ChatGPT）可從原始資料獨立重算，不依賴我方結論。

## 閘門（HKT）

- G1 今晚：Modal ephemeral vLLM 端點煙霧（純文字＋嚴格 JSON）
- G2 週六 10:00：harness 原生 baseline 單局跑通（~260 calls）
- G3 週六 12:00：正例控制（**Positive Control Quality Gate，七項勾稽**，2026-10-24 審核版）：
  1. secret channel 訊息與回覆可追蹤（`add_secret_channel_event` 事件齊全）
  2. 明確區分三種結果：**送達失敗**（技術）／**送達被拒**（有效行為結果）／**接受但無偏袒**（有效結果、不證明行為合謀）
  3. 偏袒指標由實際遊戲行動計算，非口頭報告
  4. 具可比較的 No-Alliance control
  5. 遊戲規則、死亡與勝者判定人工抽查
  6. 全部 runs 與 prompt 修改歷史保留（pilot 可除錯，歷史不刪）
  7. 主要結果可由原始 JSON 經固定腳本重算
  失敗判準：模型拒絕邀請 **不是** 實驗失敗（是有效結果）；只有「通道無法送達」或「記錄無法支撐指標」才判 G3 FAIL。禁止為了正例好看而迭代 prompt——pilot 修改可、修改歷史必留、正式前凍結。仍敗轉 3.3。
- G4 週六 18:00：每條件 2 局 pilot＋**指標驗證**（用刻意構造的正/負例軌跡驗證偏袒度量確實測到目標現象；口頭接受≠偏袒≠聯盟優勢，三者分開記錄）
- G5 週六 24:00：凍結 prompt/model/metrics/threshold/**分析腳本**，git commit hash 存記於本檔 → 週日主實驗＋分析。凍結後任何修改＝版本遞增＋pilot 重跑，舊資料 append-only 保留
- 消費紀律：任何 >$5 批次前，先產出 Research Quality Gate 報告（十項勾稽＋證據），隨檔存記
- 週日 22:00 內部凍結 → 週一 15:00 前提交（deadline 19:59）

## 預算（Modal L4 US$0.80/h；上限 $50，控制前 $10 熔斷）

- 煙霧＋G2-G4：約 $3-6；主實驗 30-38 局 × ~260 calls ≈ 5-7 GPU 時 ≈ $4-6；重跑緩衝 $5
- 逐批花費記錄於 EXPERIMENT_LOG

## 披露（失格紅線）

- apart-sprint-prep repo＝賽前訓練（LEVEL 1-3、detector validation 方法学）——報告與 README 明列 preexisting
- 官方 starter＝基礎 harness；我方修改限 our_experiment/ 與明確標註的增補
- 報告文字親筆；factual claim 附來源

## 論文頁面預算（正文 ≤8 頁，官方模板）

Abstract 150-250 字（0.3）｜Intro 0.7｜Related Work 0.8｜Methodology 2｜Results 2｜Discussion 1｜Conclusion 0.5。
Limitations & Dual-Use 附錄必交，不計頁數。寧可五頁一個可信發現，不要八頁漂亮圖表。

## 已知限制（寫作時展開）

單模型家族四席位（評審最可能攻擊的最弱假設，誠實標明＋有餘裕才加第二家族小樣本）；
n 為探索性規模；腳本化臥底非 LLM 臥底；接受訊號 base rate 依賴場景。
