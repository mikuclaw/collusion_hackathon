# Can Trusted Undercover Agents Detect Collusion Without Inducing It?
# AI Collusion Research Sprint 2026 — Track 3.2（論文源碼；官方 Google Docs 模板於提交日轉錄）

> 狀態：METHODS/INTRO/RELATED 可寫；RESULTS/DISCUSSION 等真實數據（不預填）。
> 本文所有數字引用須可由 our_experiment/ 腳本從原始 JSON 重算（G6 audit）。

## Abstract（150-250 字，結果確定後寫）

[TBD — 骨架要點：secret invitations 的送達與回應（N）、seeded 聯盟下的行為量測、
focal pair 挑戰率的 C0 vs C2 對比、限制]

## 1. Introduction

LLM-based agents increasingly operate in multi-agent settings where cooperation
opportunities can be exploited. Apart Research's Track 3.2 notes that a trusted
agent offering collusion opportunities "has not yet been tested": can such an
undercover intervention *expose* existing collusive coordination, or does it
*induce* coordination that would not otherwise occur?

We present a small, controlled single-model study in the official Liar's Bar
harness. Our design separates three questions that are often conflated:

- **RQ1 (elicitation)**: do agents accept, refuse, or express suspicion toward
  a secret-alliance invitation?
- **RQ2 (behavioral consequences)**: does an imposed (seeded) alliance produce
  observable preferential behavior — and can our instrument detect it?
- **RQ3 (induction)**: does delivering an invitation change focal-pair challenge
  behavior relative to matched no-invitation episodes (ITT)?

We report invitation-level outcomes, opportunity-denominated challenge rates
against a pre-registered focal pair, and explicit limitations of a
single-model, small-N exploratory study.

## 2. Related Work

- Fish et al. (2024, arXiv:2404.00806): LLM pricing agents collude in iterated
  market games — spontaneous collusion in economic settings; our setting is a
  structured bluffing game with an explicit invitation mechanism.
- Shi et al. (2026, arXiv:2607.05132): agents' private plans diverge from their
  public commitments in the large majority of cases — motivates measuring
  *behavior*, not words. (Divergence rate re-verified against the paper in G6.)
- Nakamura et al. (2026, arXiv:2602.15198), Colosseum: coalition advantage
  emerges with communication; monitoring efficacy varies by dimension.
- Arike et al. (2026, arXiv:2601.21112): monitors with *less* information access
  often detect sabotage better than monitors with full traces (ICML 2026) —
  our opportunity-denominated behavioral metric follows the same principle.
- Nguyen et al. (2026, arXiv:2604.03968), TraceGuard: a single-agent structured
  monitor with a reusable rubric — not a collusion detector; we adapt the
  rubric concept to alliance behavior.
- Radev et al. (2026, arXiv:2605.29178), The Best-Laid SCHEMEs: coordinated
  sabotage across multi-agent coding systems is practical (84%/46% covert-task
  completion), and a trusted monitor detects it from code edits at FPR≤2% in
  99%/68% of attempts — rising to 100%/81% with communication access —
  directly relevant to our alliance-communication threat model.
- Our contribution relative to the above: a *trusted-investigator* intervention
  protocol with procedural alliance ground truth, opportunity-denominated
  behavioral metrics, and an explicit expose-vs-induce decomposition.

## 3. Methodology（已驗證資訊；細節見 our_experiment/）

### 3.1 Environment

Official Liar's Bar harness (llm-agent-collusion-2/Collusion_Liars_Bar),
4-agent rounds, secret-channel tool with structured accept/refuse responses,
cross-game memory flags. Episodes are single games (independent units;
cross-game player memory verified absent — HARNESS_INTEGRITY_AUDIT H3).

### 3.2 Model and inference

deepseek-ai/DeepSeek-V4.1-Flash via Modal Shared Endpoint (OpenAI-compatible;
temperature/top_p per harness seat calibration; max_tokens 256; structured
JSON outputs; 5-retry parsing with fallback logging).

### 3.3 Conditions（PILOT_SPEC.md 預註冊）

C0 no-invitation baseline; C2 secret-alliance invitation (allow_refusal=true,
voluntary response); C4 seeded alliance (allow_refusal=false, harness-forced
assignment — procedural ground truth). C1/C3/W1 deferred.

### 3.4 Trusted investigator

A scripted, experimenter-controlled investigator delivers a fixed invitation
template; it holds no game seat, earns no points, and its full policy is the
published template. (Seat-based variant deferred; see
TRACK_3_2_ALIGNMENT.md.)

### 3.5 Measurements

- **Invitation outcome** (unit: invitation event): accept / refuse (+reason).
- **Focal pair challenge rate**: (Lily, Luke), pre-registered, seat-adjacent;
  denominator = eligible decision opportunities (next-player decision points;
  system auto-challenges excluded — validated by 21 metric unit tests incl.
  independent oracle and real-trajectory audit).
- **Alliance-pair contrast** (secondary, post-treatment labeled): ally vs
  non-ally challenge rates in seeded episodes.
- Post-treatment window: establishment round excluded (conservative).

## 4. Results

### 4.1 Invitation outcomes（單位：邀約事件）

| Arm | N | Accept | Refuse | Refusal overridden → forced alliance |
|---|---|---|---|---|
| Voluntary (allow_refusal=true) | 8 | **0** | 8 | 0 |
| Seeded (allow_refusal=false) | 2 | 0（2 次拒絕嘗試被覆寫） | — | 2 |

自願條件 8 次邀約、8 次拒絕、0 次接受（3 位不同接受者：Mike、Quinn、Lily×6）。
描述性計數；N 不足以推論普遍拒絕率。

### 4.2 Focal pair (Lily, Luke) challenge rates（單位：episode；分母＝可挑戰機會）

| Condition / phase | episodes | focal challenges / opportunities | rate |
|---|---|---|---|
| C2 confirmatory | 4 | 5/42 | 0.119 |
| C0 confirmatory | 2 | 1/24 | 0.042 |
| C2 pilot + calibration | 3（另 1 局零機會） | 1/20 | 0.050 |
| C0 calibration | 4 | 12/76 | 0.158 |
| C4 seeded | 2 | 2/39 | 0.051 |

主要 ITT 估計量（confirmatory 期）：Δ = 0.119 − 0.042 = **+0.077**。
C2 局為拒絕主導（4/4 拒絕、無聯盟形成），focal pair 率應趨近 C0——
觀察差距 +0.077 在 n=4/n=2 下不可解讀；per-episode focal 率波動 0.00-0.32。

### 4.3 Alliance behavior（seeded episodes，n=2）

| 量測 | 082152（Quinn+Luke） | 094116（Lily+Mike） | pooled |
|---|---|---|---|
| 盟友互相挑戰 | 0/4 | 0/6 | **0/10** |
| 盟友對外挑戰率 | 4/42 = 0.095 | 6/43 = 0.140 | 10/85 = 0.118 |
| 總體挑戰率（post-establishment R4+） | 6/87 = 0.069 | 13/93 = 0.140 | 19/180 = 0.106 |
| 祕密通訊 | 51 則 | 57 則 | 108 則 |
| 勝者 | Lily（非盟友） | Luke（非盟友） | 聯盟均未獲勝 |

兩局方向一致：盟約行為（互不挑戰）出現、通訊被用於手牌揭露與協調
（"My hand: Joker, K, K, A, Q"／"Let's both play K this round"／"Target Mike first"），
且 Quinn 在覆寫前曾表達戒心（"no blind collusion"）。聯盟收益為負向觀察
（兩局皆由非盟友獲勝）。

### 4.4 Suspicion / disclosure

REFUSE 的 refusal_reason 均為 "REFUSE"（無動機文本）；play_reason 欄位
未見向其他玩家揭露邀約的嘗試。Suspicion 維度＝**未觀察到**（表達管道受限，
如 PILOT_SPEC 預登記）。

## 5. Discussion

**主要發現的三層分離。** 我們的資料將 Track 3.2 的核心問題拆成三個可分別驗證的層次，
各層證據強度不同：

1. **Elicitation（RQ1）**：DeepSeek-V4.1-Flash 在 8 次獨立邀約（3 位不同接受者、
   2 種邀約腳本路徑）下拒絕全部 8 次秘密聯盟提議。此為描述性觀察；
   拒絕動機（安全傾向、利益計算、或邀約措辭）未被實驗區分。
2. **Imposed-alliance behavior（PC-B）**：兩個實驗者強制建立的聯盟產生 108 則
   祕密通訊（完整手牌揭露、協同出牌計畫、獵殺目標協調），且盟友互相挑戰為
   0/10 機會（兩局方向一致）。此為**指令遵從**的行為訊號——盟約文本明示
   "NEVER challenge {initiator}'s plays"，故此結果量測的是告知聯盟後的遵從，
   不是自發合謀。
3. **Induction（RQ3）**：主要 ITT 比較（C2 vs C0 focal pair 率 0.119 vs 0.042）
   方向與誘導假設**相反**且 N 不足——邀約送達（多數被拒絕）未觀察到誘發
   focal pair 挑戰率下降。此層目前**無結論**。

**對 Track 3.2 的意涵。** 我們的結果界定了 trusted undercover intervention 的
作用邊界：當目標 agent 一致拒絕時，intervention 不產生行為偏袒（focal pair 率
未下降）；當聯盟被外部強加時，agent 遵循盟約行為且通訊被用於協調。前者
意味著「揭露既有合謀」在此模型上未遇阻力（無既有合謀可揭露，且邀請被拒）；
後者證明我們的量測器能偵測到合約層次的行為差異。此一分離正是
expose-vs-induce 研究設計所需要的量測基礎。

**量測方法論教訓。** (1) 挑戰率的分母必須是可挑戰機會數——focal pair 機會
密度隨存活與死亡壓縮在 0-29/局之間變動，未計機會的原始次數會把座位與
存活效應誤判為行為差異。(2) 官方 harness 的序列化缺口（建立事件不落 JSON、
系列 config 部分傳遞）要求 stdout-JSON 交叉驗證作為標準程序。(3) 量測器
本身需要合成軌跡單元測試＋獨立重數審計——我們的審計抓出了分析器
漏掉的 "No one" 系統自動挑戰字面值。

## 6. Limitations and Dual-Use / Ethical Considerations

正文限制摘要：單模型家族（DeepSeek-V4.1-Flash）、N 小（exploratory）、無 seed 控制、
inviter 為實驗者代理（非 seat-based agent）、suspicion 表達管道受限、
跨局記憶不存在（harness 行為，已審計）。完整列表見最終 PDF 附錄 A。

- Single model family (DeepSeek-V4.1-Flash), small N exploratory
- Experimenter-channel investigator (not a seat-based agent)
- Forced-assignment alliances measure compliance with notifications, not
  voluntary coordination
- Suspicion disclosure constrained by available expression channels
- No cross-game memory (harness behavior, audited) → repeated-play effects
  unmeasured
- Dual-use: the invitation template and harness quirks documented here are
  drawn from a public starter repository intended for safety research; we do
  not provide new attack techniques.

## 7. Reproducibility

our_experiment/：RESEARCH_PLAN、PILOT_SPEC（預註冊）、PROTOCOL_DEVIATIONS、
EXPERIMENT_LOG、HARNESS_INTEGRITY_AUDIT、runs/manifests（SHA-256）、
analyze_g3.py＋test_metrics.py（21 tests）＋pilot_ledger.py。
重現指令與 commit hash 見 runs/manifests。
