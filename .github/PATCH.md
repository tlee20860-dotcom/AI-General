## 修改目標: `.github/workflows/setup-structure.yml`

<<<<<<< OLD
          echo "> 構建編號：#${{ github.run_number }}" >> "$OUTPUT"
=======
          echo "> 生成時間：$(TZ=Asia/Hong_Kong date '+%Y-%m-%d %H:%M:%S') (HKT)" >> "$OUTPUT"
>>>>>>> NEW

<<<<<<< OLD
          echo "# AI 對話系統 - 體系狀態包" > "$OUTPUT"
          echo "" >> "$OUTPUT"
=======
          echo "# AI 對話系統 - 體系狀態包" > "$OUTPUT"
          echo "" >> "$OUTPUT"
          echo "> 生成時間：$(TZ=Asia/Hong_Kong date '+%Y-%m-%d %H:%M:%S') (HKT)" >> "$OUTPUT"
          echo "" >> "$OUTPUT"
>>>>>>> NEW

## 修改目標: `docs/common/C-00-startup.md`

<<<<<<< OLD
**AI 讀到共享包後必須回報**：「本包構建編號 #NNNN，生成於 XX」，並問使用者是否為最新。
=======
**AI 讀到共享包後必須回報**：「本包生成於 XX (HKT)」，並問使用者是否為最新。
>>>>>>> NEW

## 修改目標: `docs/common/C-11-terms.md`

<<<<<<< OLD
| 27 | 構建編號 | 共享包頂部的 `#NNNN`，由 Actions 的 `run_number` 產生。AI 讀到後須回報並問使用者是否為最新。 |
=======
| 27 | 生成時間 | 共享包頂部的 `YYYY-MM-DD HH:mm:ss (HKT)`，由 Actions 產生。AI 讀到後須回報並問使用者是否為最新。 |
>>>>>>> NEW