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

- Fish et al. (2024): LLM pricing agents tacitly collude (arXiv:2404.00806) —
  spontaneous collusion in market settings; our setting is a structured
  bluffing game with an explicit invitation mechanism.
- Shapiro et al. (2026, Track 3.2 core): private plans vs. public commitments
  diverge in >90% of cases — motivates measuring *behavior*, not words.
- Terdich et al. (2026, Colosseum): coalition advantage emerges with
  communication; monitoring split by dimension.
- Nguyen et al. (2026, TraceGuard): multi-dimensional structured monitoring.
- Kaneko et al. (2026): less-is-more monitoring; single-dimension behavioral
  monitoring outperformed.
- Radev et al. (2026, SabotageMonitors): monitors as sabotage targets.
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

[TBD — pilot ledger + confirmatory runs；由 pilot_ledger.py 產生]

## 5. Discussion

[TBD]

## 6. Limitations and Dual-Use / Ethical Considerations

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
