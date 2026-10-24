#!/usr/bin/env bash
# 複現批次（D9）：C2×4 + C4×2 + C0×2，共 8 episodes
# 檢驗 Revision 8 結論可重現性；分析程序＝凍結版不變
set -u
cd "$(dirname "$0")/../llm-agent-collusion-2/Collusion_Liars_Bar" || exit 1
RUN=../../our_experiment/run_logged.sh
EP=../../our_experiment/with_endpoint.sh

i=1
while [ $i -le 4 ]; do
  "$RUN" "../../our_experiment/logs/rep_c2_$i.log" \
    "$EP" deepseek ../../.venv/bin/python src/game/game_secret_channel.py \
    --trigger-round 2 --chosen-player Lily --allow-refusal
  i=$((i+1))
done

i=1
while [ $i -le 2 ]; do
  "$RUN" "../../our_experiment/logs/rep_c4_$i.log" \
    "$EP" deepseek ../../.venv/bin/python src/game/game_secret_channel.py \
    --trigger-round 2 --chosen-player Lily
  i=$((i+1))
done

i=1
while [ $i -le 2 ]; do
  "$RUN" "../../our_experiment/logs/rep_c0_$i.log" \
    "$EP" deepseek ../../.venv/bin/python src/game/game.py
  i=$((i+1))
done
echo "REPLICATION_BATCH_DONE"
