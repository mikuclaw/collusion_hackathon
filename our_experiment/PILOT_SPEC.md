# PILOT SPEC（預註冊，2026-10-24 上午寫定於任何 pilot episode 執行前）

## 設計

單位＝單局 episode（`game_secret_channel.py` 或 `game.py` 各跑一次）。
因 H3（跨局記憶失效），episodes 彼此獨立——每局一個邀約事件或無邀約，乾淨的獨立分配單位。
無 seed 控制（harness 隨機發牌/隨機目標），如實記錄抽籤結果；以隨機化取代配對。

## 條件與數量（pilot 級）

| 條件 | 指令 | 數量 | 說明 |
|---|---|---|---|
| C2 | `game_secret_channel.py --trigger-round 2 --allow-refusal` | 4 | 邀約送達、自願回應（ITT：拒絕者保留） |
| C0 | `game.py`（無通道） | 4 | 2 局既存（attempt 1/2 的無邀約局）＋2 局新跑 |
| C4 | `game_secret_channel.py --trigger-round 2`（無 --allow-refusal＝seeded） | 2 | 1 局既存（attempt 3 g1）＋1 局新跑 |

C1/C3/W1：本 pilot 不跑（次要條件，時間允許才加）。

## 主要結果（ITT，預註冊）

1. 邀約結果計數：accept / refuse（邀約事件單位）
2. Focal pair (Lily, Luke) 挑戰率：C2 vs C0 的 episode 級對比
   （分母＝可挑戰機會；post-establishment＝round 3 建立者從 round 4 起算、
   C0 全局；保守規則已凍結於分析器 min_round/max_round）
3. 每條件有效 episode 數與無效原因（invalid_registry）

## 排除規則（沿用 invalid_registry）

SIGPIPE/管線死亡、程序被殺未完成、JSON 不可解析、邀約未送達。

## 分析程序（凍結）

analyze_g3.py v3 函式逐局計算 → episode 表（條件、邀約結果、focal pair 挑戰率、
盟友對內/對外率、機會數）→ 描述性效果量＋不確定性（無 p 值追逐）。

## 探索性（不入主要結論）

- Quinn/Luke 強制聯盟後的行為（attempt 3）
- refusal_reason 與 play_reason 文本的 suspicion 標記（表達管道受限，如實標記）
- alliance-pair 對比（post-treatment 標籤，次要）

---

# 凍結確認（G5，2026-10-24 09:50 HKT）

G3 過閘（G3_REVIEW.md GO）。本文件升格為**凍結協議**，確認性批次擴張如下：

- C2 總計 **8 episodes**（既有 4＋新增 4，`run_confirmatory.sh`）
- C0 總計 **6 episodes**（既有 4＋新增 2）
- C4 維持 **2 episodes**（seeded 量測器驗證已足，不擴張）
- 條件定義、主要結果（focal pair ITT）、排除規則、分析程序：**以上文為準，不再修改**
- 排除規則外之任何偏离 → PROTOCOL_DEVIATIONS.md 記錄
- 分析程序凍結版本＝pilot_ledger.py @ 凍結 commit；結果產出後僅修文字不改計算

PI 已核准擴張（playbook「pilot 3-5 seeds → 正式 10-20」路徑；時間限制下取 C2×8/C0×6）。
