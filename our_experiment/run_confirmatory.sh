#!/usr/bin/env bash
# 確認性批次（G5）：C2×4 + C0×2，共 6 episodes，順序執行、全量日誌、零管線。
# 凍結依據：PILOT_SPEC.md + EXPERIMENT_LOG G5 freeze 行（commit 見 git log）。
set -u
cd "$(dirname "$0")/../llm-agent-collusion-2/Collusion_Liars_Bar" || exit 1
RUN=../../our_experiment/run_logged.sh
EP=../../our_experiment/with_endpoint.sh

for i in 1 2 3 4; do
  "$RUN" "../../our_experiment/logs/main_c2_$i.log" \
    "$EP" deepseek ../../.venv/bin/python src/game/game_secret_channel.py \
    --trigger-round 2 --chosen-player Lily --allow-refusal
done
for i in 1 2; do
  "$RUN" "../../our_experiment/logs/main_c0_$i.log" \
    "$EP" deepseek ../../.venv/bin/python src/game/game.py
done
echo "CONFIRMATORY_BATCH_DONE"
