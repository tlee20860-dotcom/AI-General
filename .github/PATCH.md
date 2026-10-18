# PATCH 指令

## 修改目標: `.github/workflows/setup-structure.yml`

<<<<<<< OLD
    web-app-family|external/web-app-family|tlee20860-dotcom/WEB-APP-Family|90|PACKAGE-web-app-family.md|W|家庭 webapp
=======
    web-app-family|external/web-app-family|tlee20860-dotcom/WEB-APP-Family|90|PACKAGE-web-app-family.md|W|家庭 webapp
    ai-os|external/ai-os|tlee20860-dotcom/AI-OS|91|PACKAGE-ai-os.md|E|AI-OS 輕量版
>>>>>>> NEW

<<<<<<< OLD
            proj_docs_dir="$path/docs/projects/${name}"
            if [ -d "$proj_docs_dir" ]; then
              # 使用 P-* 白名單前綴匹配，避免收錄無關檔案（含 P-98）
              for prefix in P-01 P-02 P-05 P-06 P-07 P-08 P-09 P-12 P-13 P-98 P-99; do
                for f in ${proj_docs_dir}/${prefix}-*.md; do
                  if [ -f "$f" ]; then bash .github/workflows/append_file.sh "$f" "$OUTPUT" || true; fi
                done
              done
            fi
=======
            # 若為 AI-OS 專案，直接讀取根目錄的 E-*.md，並加入標題
            if [ "$name" = "ai-os" ]; then
              echo "# AI-OS 輕量版引導系統（V: $(date +%s)）" >> "$OUTPUT"
              echo "" >> "$OUTPUT"
              for f in "$path"/E-*.md; do
                if [ -f "$f" ]; then bash .github/workflows/append_file.sh "$f" "$OUTPUT" || true; fi
              done
            else
              proj_docs_dir="$path/docs/projects/${name}"
              if [ -d "$proj_docs_dir" ]; then
                # 使用 P-* 白名單前綴匹配，避免收錄無關檔案（含 P-98）
                for prefix in P-01 P-02 P-05 P-06 P-07 P-08 P-09 P-12 P-13 P-98 P-99; do
                  for f in ${proj_docs_dir}/${prefix}-*.md; do
                    if [ -f "$f" ]; then bash .github/workflows/append_file.sh "$f" "$OUTPUT" || true; fi
                  done
                done
              fi
            fi
>>>>>>> NEW

<<<<<<< REGEX
V: \d+
=======
V: 1792316000
>>>>>>> NEW

<<<<<<< REGEX
W: ai-system-20261018-[^\n]+
=======
W: ai-system-20261018-008#095
>>>>>>> NEW