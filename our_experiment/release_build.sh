#!/usr/bin/env bash
# 一次性發布鏈：編譯（驗證退出碼）→ 雜湊 → 同步 → 推送 → 回報
# 防再犯：上一輪 typst compile | head 掩蓋失敗 + 競態雜湊舊檔（G7 事故）
set -euo pipefail
cd "$(dirname "$0")/paper"

# 1. 編譯——不接任何管線，直接驗退出碼
typst compile main_en.typ main_en.pdf

# 2. 雜湊剛編譯的這個檔案（唯一事實源）
SHA_LOCAL=$(shasum -a 256 main_en.pdf | cut -d' ' -f1)
PAGES=$(mdls -name kMDItemNumberOfPages main_en.pdf 2>/dev/null | grep -oE '[0-9]+' || echo "?")

# 3. 同步到研究包 repo 並驗證副本雜湊一致
cp main_en.typ main_en.pdf /Users/miku/Github/collusion-track32-study/paper/
SHA_REPO=$(shasum -a 256 /Users/miku/Github/collusion-track32-study/paper/main_en.pdf | cut -d' ' -f1)
[ "$SHA_LOCAL" = "$SHA_REPO" ] || { echo "FATAL: repo copy hash mismatch"; exit 1; }

echo "COMPILE_OK pages=$PAGES"
echo "SHA_FINAL=$SHA_LOCAL"
echo "SHA_REPO_MATCH=yes"
