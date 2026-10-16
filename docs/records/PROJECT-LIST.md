# 專案清單

最後更新：A20261016-001
Version: 1791908200
Batch: B34-4
Writer: A20261016-001
用途：記錄所有專案的名稱、領域、倉庫、專案包檔名

---

## 專案一

name: web-app-family
display: 家庭 webapp
code: webapp
domain: W
repo: tlee20860-dotcom/WEB-APP-Family
repo_visibility: public
package: PACKAGE-web-app-family.md
handoff: docs/projects/web-app-family/P-13-handoff.md
auto_create: false
init_content: none

---

## 專案二

name: ai-training
display: 訓練 AI
code: ai-training
domain: W
repo: tlee20860-dotcom/AI-training-files
repo_visibility: public
package: PACKAGE-ai-training.md
handoff: docs/projects/ai-training/P-13-handoff.md
auto_create: false
init_content: none

---

## 專案三（體系層）

name: ai-system
display: AI 對話系統
code: ai-system
domain: system
repo: tlee20860-dotcom/AI-General
repo_visibility: public
package: （無，體系層不生成專案包）
handoff: （無）
auto_create: false
init_content: none

---

## 新增專案規則

新增專案時，請在下方新增一個區塊，格式如上。

欄位說明：

| 欄位 | 說明 |
|---|---|
| name | 專案英文名（目錄名與倉庫名） |
| display | 專案顯示名稱（中文） |
| code | 專案代碼（用於對話編號前綴，英文小寫） |
| domain | 領域（W / V / D / M / system / 其他） |
| repo | 倉庫完整名稱 |
| repo_visibility | public 或 private |
| package | 專案包檔名 |
| handoff | 專案交接檔案路徑 |
| auto_create | 是否由 Actions 自動建立倉庫 |
| init_content | 新倉庫初始內容 |

---

/* ═══ EOF ═══
F: AI-General/docs/records/PROJECT-LIST.md
V: 1791908200
B: B34-4
W: A20261016-001
═══ */