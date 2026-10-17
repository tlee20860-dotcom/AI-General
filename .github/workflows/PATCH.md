# ============================================
# patch.yml — 自動替換 Patch 腳本
# 位置：AI-General/.github/workflows/patch.yml
# ============================================

name: Execute Patch

on:
  push:
    paths:
      - '.github/workflows/PATCH.md'

jobs:
  patch:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Run Patch Script
        run: |
          PATCH_FILE=".github/workflows/PATCH.md"
          echo "=== 讀取 PATCH 指令 ==="
          
          # 解析目標檔案
          TARGET=$(grep -m 1 '^`docs/' "$PATCH_FILE" | tr -d '\r' | tr -d '`' || true)
          if [ -z "$TARGET" ]; then
            echo "❌ 找不到目標路徑 (需用反引號包裹)"
            exit 1
          fi
          
          if [ ! -f "$TARGET" ]; then
            echo "❌ 目標檔案不存在：$TARGET"
            exit 1
          fi

          # 提取 OLD 與 NEW (使用 awk)
          awk '/^<<<<<<< OLD/{flag=1;next}/^=======/{flag=0}flag' "$PATCH_FILE" > /tmp/old.txt
          awk '/^=======/{flag=1;next}/^>>>>>>> NEW/{flag=0}flag' "$PATCH_FILE" > /tmp/new.txt

          if [ ! -s /tmp/old.txt ]; then
            echo "❌ 找不到舊內容 (需包含 <<<<<<< OLD)"
            exit 1
          fi

          # 檢查唯一性 (避免改錯)
          MATCH_COUNT=$(grep -F -c -f /tmp/old.txt "$TARGET" || true)
          if [ "$MATCH_COUNT" -eq 0 ]; then
            echo "❌ 錯誤：在目標檔案中找不到舊內容。"
            exit 1
          fi
          if [ "$MATCH_COUNT" -gt 1 ]; then
            echo "❌ 錯誤：舊內容在目標檔案中出現多次 ($MATCH_COUNT)，容易改錯，中止。"
            exit 1
          fi

          # 執行替換 (用 Python 安全處理多行文本)
          python3 -c "
import sys
target = sys.argv[1]
with open('/tmp/old.txt', 'r') as f: old = f.read().strip('\n')
with open('/tmp/new.txt', 'r') as f: new = f.read().strip('\n')
with open(target, 'r') as f: content = f.read()
with open(target, 'w') as f: f.write(content.replace(old, new, 1))
" "$TARGET"

          echo "✅ 替換成功：$TARGET"
          
          # 刪除 PATCH.md 避免重複觸發
          git rm -f "$PATCH_FILE"

      - name: Commit and Push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .
          if git diff --cached --quiet; then
            echo "無變更"
          else
            git commit -m "chore: auto-apply patch [skip ci]"
            git push
          fi