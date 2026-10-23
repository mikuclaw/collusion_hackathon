#!/usr/bin/env bash
# run_logged.sh <log檔> <cmd...>
# 活體實驗程序的全量日誌包裝器：stdout/stderr 完整落檔，不經 grep/head（SIGPIPE 防線）。
# 分析一律在執行結束後對 log 檔離線進行。退出碼原樣傳回。
# 用法：run_logged.sh our_experiment/logs/foo.log <command...>
set -u
LOG="$1"; shift
mkdir -p "$(dirname "$LOG")"
"$@" > "$LOG" 2>&1
code=$?
lines=$(wc -l < "$LOG" | tr -d ' ')
echo "run_logged: exit=$code log=$LOG lines=$lines"
exit $code
