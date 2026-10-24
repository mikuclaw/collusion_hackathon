# PROTOCOL DEVIATIONS

規則：實驗期間任何 prompt、模型、指標、樣本計畫或程式碼的修改都在此記錄。修 bug 可以，暗中改研究假設不行。

| # | 日期 | 偏差 | 原因 | 影響評估 | 處置 |
|---|---|---|---|---|---|
| D1 | 2026-10-24 | G3 attempt 2 起移除 `--chosen-player`，邀約目標改為隨機 | 官方 starter 的系列 config 傳遞怪癖：系列層 config 實證含 `chosen_player: Lily`，遊戲層卻以 random 執行（紀錄 config={}），指定目標不可靠 | 正例有效性不受影響（隨機對象的邀約仍為邀約）；定向邀約（RQ4 的「臥底主動選擇目標」）延後到修補或改用單局腳本 | 保留 attempt 1 證據鏈；attempt 2 以隨機目標執行 |
| D2 | 2026-10-24 | 挑戰率指標分母改為「可挑戰機會數」，排除系統自動挑戰（next_player 空白） | 審核修正：原始計畫的「挑戰次數差異」無法區分機會不均與刻意偏袒 | attempt 1 數字微幅變動（如 074117 0.083）；量測器經 12 項合成軌跡單元測試驗證（test_metrics.py） | 凍結前即修正，無正式資料受影響 |
| D3 | 2026-10-24 | no-alliance baseline（235901）為單局，與系列局非完全配對 | 時間順序：baseline 先於配對對照設計定案 | 近似反事實（同 harness/model/參數），非嚴格配對；G4 的 C0/C4 arm 才是正式配對對照 | findings 引用時標明「近似配對」 |
| D4 | 2026-10-24 | 主要估計量改為 Focal Pair 設計（C0 無 ally 標籤，原 C2-vs-C0 比較不可定義） | 獨立審核 P0 修正 | 主估計量＝focal pair (Lily, Luke) 挑戰率 Δ；alliance-pair 對比降為次要（post-treatment 標明） | RESEARCH_PLAN 已更新；文獻映射不變 |
| D5 | 2026-10-24 | 分析器加回合過濾（min_round/max_round）＋排除 "No one" 字面值自動挑戰 | 審核要求 post-establishment 過濾；真實軌跡審計抓出 "No one" 洩漏 | 21 項測試護航（含 T9 局中建盟）；attempt 1/2 已出版數字受影響者重算（a2-g1 post 3→4） | test_metrics.py 全綠 |
| D6 | 2026-10-24 | a2-g1 post 窗 v1 誤植為 3（邀約實際落在 round 3，offer 回合不應入分母），v2 修正為 4；連帶 p-c2-1/2、m-c2-1..4 統一 post=事件回合+1 | 凍結規則「排除 offer 回合」的實作遺漏。**真實數字位移：pilot 期 C2 pooled 修正為 1/20=0.050**（v1 的 2/22=0.091 為混合窗暫態：a2-g1 含 offer 回合 1/6＋p-c2 舊窗 1/16）；G3_REVIEW pilot 行與 SKEPTICAL_REVIEW 疑點一之一初版曾引用 0.091，已出 v2 修正 | 本表＋G3_REVIEW＋SKEPTICAL_REVIEW 三處同步；另 sed -i 二次用於凍結分析器檔案（紀律違規，自此僅 edit 工具） |
| D7 | 2026-10-24 | 凍結 commit（d08fc09）後分析器差量清單 | 獨立審核將 diff 凍結 commit 與 HEAD，逐項預備解釋 | (1) pilot_ledger.py：EPISODES 升 5-tuple（+phase 欄）＋phase×condition 分組彙總——**重構，不動計算**；(2) winner-null 完整性守衛——**實作已凍結的 INVALID 排除規則**（局中 partial 不入池，防 bg_104 孤兒部分檔污染）；(3) D6 post 窗修正——**回歸凍結規則**（排除 offer 回合）。三項均不改研究假設或主要結果定義 | G3_REVIEW/SKEPTICAL_REVIEW/PILOT_SPEC 三處同步 |
| D8 | 2026-10-24 | 樣本量修正：planned C2×8/C0×6/C4×2 → **amended C2×10/C0×8/C4×2**（+2/+2/+0，對稱加樣） | **planned C0×2 已由孤兒程序完整交付**（112955＋113902＝m-c0-1/2，已在 ledger）——擴張批次非補缺，是**對稱加樣至 playbook 區間下限**（C2×10/C0×8）。批次追蹤 shell 3600s 超時（孤兒仍跑完全部 6 局） | 對稱加樣、無逐臂挑選；**optional-stopping 限制**：序列加樣若無校正，估計量有偏往早期趨勢之風險——論文以描述性估計＋不確定性呈現，不做顯著性宣稱；此為最後一次擴張。**能見度聲明**：D8 入冊時 main_c2_1..4 紀錄已落盤可見（bg_104 完成）、m-c0_1 執行中、m-c0_2 未開始——加樣為 +2/+2 對稱，非針對已見結果方向的事後選擇 | PILOT_SPEC 凍結節加 D8 指標；估計量維持 focal pair ITT 不換 |
