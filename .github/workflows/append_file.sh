#!/bin/bash
# ============================================
# append_file.sh — 穩健地將檔案附加到 Markdown
# 位置：AI-General/.github/workflows/append_file.sh
# 用途：處理反引號、換行、檔案標記
# ============================================

FILE="$1"
OUTPUT="$2"

if [ ! -f "$FILE" ]; then
  echo "（檔案不存在：$FILE）" >> "$OUTPUT"
  exit 0
fi

# 檢測檔案內容中最大連續反引號數
max_backticks=$(grep -oE '`+' "$FILE" 2>/dev/null | awk '{ print length }' | sort -rn | head -1)
if [ -z "$max_backticks" ]; then
  max_backticks=0
fi

# 外層反引號數 = 內層最大 + 1，最少 3 個
outer_count=$((max_backticks + 1))
if [ "$outer_count" -lt 3 ]; then
  outer_count=3
fi

# 生成反引號字串
backticks=$(printf '%*s' "$outer_count" '' | tr ' ' '`')

# 輸出檔案區塊
{
  echo ""
  echo "<!-- === FILE START: $FILE === -->"
  echo ""
  echo "## 📄 $FILE"
  echo ""
  echo "$backticks"
  cat "$FILE"
  # 如果檔案結尾沒有換行，補一個
  if [ -n "$(tail -c 1 "$FILE")" ]; then
    echo ""
  fi
  echo "$backticks"
  echo ""
  echo "<!-- === FILE END: $FILE === -->"
  echo ""
} >> "$OUTPUT"
