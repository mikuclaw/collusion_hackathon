#!/usr/bin/env bash
# with_endpoint.sh <deepseek|qwen38|glm53> [command...]
# 依家族設定 LLM_* 並執行 command；無 command 則印出解析後的 base_url 與 model（不含金鑰）。
# 金鑰從 repo-root compute.env 讀取，本檔不寫死任何 secret。
# 用法：
#   our_experiment/with_endpoint.sh deepseek ../../.venv/bin/python src/game/game.py
#   (cd Collusion_Liars_Bar && ../../our_experiment/with_endpoint.sh qwen38 ../../.venv/bin/python src/game/game.py)
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
set -a; source "$REPO/compute.env"; set +a
export LLM_API_KEY="${MODAL_PROXY_TOKEN_ID:?}.${MODAL_PROXY_TOKEN_SECRET:?}"
FAMILY="${1:-}"
case "$FAMILY" in
  deepseek) export LLM_BASE_URL="$EP_DEEPSEEK"; export LLM_MODEL="$MODEL_DEEPSEEK" ;;
  qwen38)   export LLM_BASE_URL="$EP_QWEN38";   export LLM_MODEL="$MODEL_QWEN38" ;;
  glm53)    export LLM_BASE_URL="$EP_GLM53";    export LLM_MODEL="$MODEL_GLM53" ;;
  "")
    echo "usage: with_endpoint.sh <deepseek|qwen38|glm53> [command...]" >&2; exit 2 ;;
  *) echo "unknown family: $FAMILY（kimi_k3 已淘汰；inkling 凍結中）" >&2; exit 2 ;;
esac
if [ $# -gt 1 ]; then
  shift; exec "$@"
else
  echo "LLM_BASE_URL=$LLM_BASE_URL"; echo "LLM_MODEL=$LLM_MODEL"; echo "LLM_API_KEY=<set:${#LLM_API_KEY} chars>"
fi
