# 專案清單

最後更新：ai-system-20261016-003
Version: 1791918000
Batch: B34-5
Writer: ai-system-20261016-003#096
用途：記錄所有專案的名稱、領域、倉庫、專案包檔名、包編號

---

## 專案一

name: web-app-family
display: 家庭 webapp
code: webapp
domain: W
repo: tlee20860-dotcom/WEB-APP-Family
repo_visibility: public
package_no: 90
package: PACKAGE-web-app-family.md
handoff: docs/projects/web-app-family/P-13-handoff.md
auto_create: false
init_content: none

---

## 專案二（體系層）

name: ai-system
display: AI 對話系統
code: ai-system
domain: system
repo: tlee20860-dotcom/AI-General
repo_visibility: public
package_no: （不適用）
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
| package_no | 共享包編號（十位數 = 類別，見下方對照） |
| package | 專案包檔名 |
| handoff | 專案交接檔案路徑 |
| auto_create | 是否由 Actions 自動建立倉庫 |
| init_content | 新倉庫初始內容 |

---

## 包編號對照

**十位數 = 類別，個位數 = 同類序號。**

| 編號 | 檔案 | 類別 | 生成方式 |
|---|---|---|---|
| 01 | 01-CORE-SYSTEM.md | 體系核心 | setup-structure.yml 寫死 |
| 02 | 02-CORE-PROJECT.md | 專案核心 | setup-structure.yml 寫死 |
| 10 | 10-SKILLS-W.md | Web App 技能 | setup-structure.yml 寫死 |
| 20 | 20-SKILLS-V.md | VBA 技能（未來） | 未來新增 |
| 30 | 30-SKILLS-D.md | 資料分析技能（未來） | 未來新增 |
| 90 | 90-web-app-family.md | 家庭 webapp | 本清單 |
| 91+ | 未來新增專案 | 依序 | 本清單 |
| 99 | 99-CONCLUSION-ARCHIVE.md | 體系舊決策（罕用） | setup-structure.yml 寫死 |

**編號分配規則**：

| 類別 | 範圍 | 說明 |
|---|---|---|
| 體系核心包 | 01~09 | 固定，不變 |
| 領域技能包 | 10~89 | 每領域一組（10、20、30…） |
| 專案包 | 90~98 | 各專案依序 |
| 罕用包 | 99 | 固定 |

---

## 歷史記錄

| 專案 | 移除時間 | 原因 |
|---|---|---|
| ai-training（訓練 AI） | 2026-10-16 | 與體系層重複，內容已遷移至 AI-General |

---

/* ═══ EOF ═══
F: AI-General/docs/records/PROJECT-LIST.md
V: 1791918000
B: B34-5
W: ai-system-20261016-003#096
═══ */