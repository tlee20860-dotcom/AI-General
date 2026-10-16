# 遷移清單

## 版本

最後更新：A20261016-001
執行階段：phase-1（複製）/ phase-2（刪除源頭）

---

## 欄位說明

| 欄位 | 說明 |
|---|---|
| source_repo | 來源倉庫（完整名稱） |
| source_path | 來源路徑（支援 * 通配符） |
| target_repo | 目標倉庫（完整名稱） |
| target_path | 目標路徑（以 / 結尾代表目錄） |

---

## 參與倉庫

- tlee20860-dotcom/AI-General
- tlee20860-dotcom/AI-training-files
- tlee20860-dotcom/WEB-APP-Family
- tlee20860-dotcom/AI-training-build

---

## 任務一：C-* 搬到 AI-General

source_repo: tlee20860-dotcom/AI-training-files
source_path: docs/common/C-*.md
target_repo: tlee20860-dotcom/AI-General
target_path: docs/common/

---

## 任務二：W-* 搬到 AI-General

source_repo: tlee20860-dotcom/AI-training-files
source_path: docs/skills/W/W-*.md
target_repo: tlee20860-dotcom/AI-General
target_path: docs/skills/W/

---

## 任務三：R-* 搬到 AI-General

source_repo: tlee20860-dotcom/AI-training-files
source_path: docs/records/R-*.md
target_repo: tlee20860-dotcom/AI-General
target_path: docs/records/

---

## 任務四：setup-structure.yml 搬到 AI-General

source_repo: tlee20860-dotcom/AI-training-files
source_path: .github/workflows/setup-structure.yml
target_repo: tlee20860-dotcom/AI-General
target_path: .github/workflows/

---

## 任務五：家庭 webapp P-* 搬到 WEB-APP-Family

source_repo: tlee20860-dotcom/AI-training-files
source_path: docs/projects/family-fin/*.md
target_repo: tlee20860-dotcom/WEB-APP-Family
target_path: docs/projects/web-app-family/

---

## 備註

- phase-1：複製檔案到目標倉庫，源頭保留。
- phase-2：確認 phase-1 成功後執行，刪除源頭檔案。
- 未來架構變更時，更新本檔案，重新執行即可。
- 訓練 AI 專案（docs/projects/ai-training/）留在 AI-training-files，不搬遷。

---

/* ═══ EOF ═══
F: AI-General/MIGRATION.md
V: 1791906500
B: B34-4
W: A20261016-001
═══ */
