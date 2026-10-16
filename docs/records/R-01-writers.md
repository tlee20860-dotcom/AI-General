# R-01 AI 編寫者名單 + 專案索引

最後更新：ai-system-20261016-002
Version: 1791910000
Batch: B34-4
Writer: ai-system-20261016-002
用途：追蹤專案 / 對話 / 編寫者 / 檔案歸屬 / Repo

---

## 一、編號規則

### 1.1 對話編號

格式：`{專案代碼}-{YYYYMMDD}-{專案內序號3位}`

| 範例 | 說明 |
|---|---|
| webapp-20261016-001 | 家庭 webapp 的第 1 個對話 |
| ai-training-20261016-001 | 訓練 AI 的第 1 個對話 |
| ai-system-20261016-001 | AI 對話系統的第 1 個對話 |

**專案代碼**：由 PROJECT-LIST.md 的 `code` 欄位決定。
**專案內序號**：從 `001` 開始，跨日期累計，各專案獨立。

### 1.2 回覆序號

格式：`#{序號}`（如 `#001`）

### 1.3 Writer 欄位格式

`{對話編號}#{回覆序號}`（如 `webapp-20261016-001#014`）

---

## 二、生成流程

| 情境 | 動作 |
|---|---|
| 有本名單 | 取該專案最新序號 + 1 |
| 無本名單 | 自建第一筆並交付本檔 |

**專案識別**：

| 步驟 | 動作 |
|---|---|
| 1 | 使用者選擇專案 |
| 2 | AI 從 PROJECT-LIST.md 讀取該專案的 `code` |
| 3 | AI 從本檔 §四 找該專案最新序號 |

---

## 三、專案清單

### 家庭 webapp（webapp）

| 欄位 | 值 |
|---|---|
| 專案名稱 | 家庭 webapp |
| 專案代碼 | webapp |
| 領域 | W（Web App） |
| 起始日期 | 2026-10-13 |
| 程式碼 repo | tlee20860-dotcom/WEB-APP-Family |
| P-* 檔案位置 | WEB-APP-Family/docs/projects/web-app-family/ |

### 訓練 AI（ai-training）

| 欄位 | 值 |
|---|---|
| 專案名稱 | 訓練 AI |
| 專案代碼 | ai-training |
| 領域 | W |
| 起始日期 | 2026-10-16 |
| 程式碼 repo | tlee20860-dotcom/AI-training-files |
| P-* 檔案位置 | AI-training-files/docs/projects/ai-training/ |

### AI 對話系統（ai-system）

| 欄位 | 值 |
|---|---|
| 專案名稱 | AI 對話系統 |
| 專案代碼 | ai-system |
| 領域 | system |
| 起始日期 | 2026-10-16 |
| 程式碼 repo | tlee20860-dotcom/AI-General |
| P-* 檔案位置 | 體系層（無 P-*，只有 C-*、W-*、R-*） |

---

## 三之一、Repo 清單

**用途**：AI 提到 repo 時，一律使用實際名稱（見 C-02 §十三之一）。

| Repo | 用途 | URL |
|---|---|---|
| AI-General | AI 對話系統（體系層） | github.com/tlee20860-dotcom/AI-General |
| AI-training-build | 生成共享包（Actions 產出） | github.com/tlee20860-dotcom/AI-training-build |
| WEB-APP-Family | 家庭 webapp 程式碼 | github.com/tlee20860-dotcom/WEB-APP-Family |
| AI-training-files | 訓練 AI 專案 | github.com/tlee20860-dotcom/AI-training-files |

**未來新增 repo 方式**：使用者在對話中說「新增 repo X（用途 / URL）」→ AI 更新本節。

---

## 四、編寫者清單

| # | 對話編號 | 所屬專案 | 建立時間 | 累計回覆 |
|---|---|---|---|---|
| 1 | ai-system-20261016-001 | AI 對話系統 | 2026-10-16 | 66 |
| 2 | ai-system-20261016-002 | AI 對話系統 | 2026-10-16 | 0 |

**說明**：

- 舊編號（A20261013-001 ~ A20261016-001）已廢止，改用新格式。
- 專案內序號從 `001` 開始，跨日期累計。

---

## 五、檔案歸屬（現役）

### AI-General/docs/common/（L1 AI 通用）

| 檔案 | Version | Writer |
|---|---|---|
| C-00-startup.md | 待更新 | 舊版 |
| C-01-profile.md | 待更新 | 舊版 |
| C-02-rules.md | 1791908400 | ai-system-20261016-001 |
| C-03-guide.md | 1791907700 | ai-system-20261016-001 |
| C-04-delivery.md | 1791908500 | ai-system-20261016-001 |
| C-05-learning.md | 待更新 | 舊版 |
| C-06-token-log.md | 待更新 | 舊版 |
| C-07-summary.md | 待更新 | 舊版 |
| C-09-rolling-mechanism.md | 待更新 | 舊版 |
| C-10-handoff-mechanism.md | 待更新 | 舊版 |
| C-11-terms.md | 1791908600 | ai-system-20261016-001 |

### AI-General/docs/skills/W/（L2 Web App 通用）

| 檔案 | Version | Writer |
|---|---|---|
| W-00-startup.md | 1791903760 | 舊版 |
| W-01-firebase.md | 1791899500 | 舊版 |
| W-02-functions.md | 1791899560 | 舊版 |
| W-03-esmodule.md | 1791899620 | 舊版 |
| W-04-pwa.md | 1791899680 | 舊版 |
| W-05-schema.md | 1791899740 | 舊版 |

### AI-General/docs/records/（L4 機械記錄）

| 檔案 | Version | Writer |
|---|---|---|
| R-01-writers.md | 1791910000 | ai-system-20261016-002 |
| PROJECT-LIST.md | 1791908200 | ai-system-20261016-001 |
| REPOS.md | （Actions 生成） | — |
| PROGRESS.md | 1791907800 | ai-system-20261016-001 |

### AI-General/.github/workflows/

| 檔案 | Version | Writer |
|---|---|---|
| setup-structure.yml | 1791908100 | ai-system-20261016-001 |
| setup-migration.yml | 1791906700 | ai-system-20261016-001 |
| append_file.sh | 1791908100 | ai-system-20261016-001 |

### AI-General 根目錄

| 檔案 | Version | Writer |
|---|---|---|
| MIGRATION.md | 1791906500 | ai-system-20261016-001 |
| MIGRATION-GUIDE.md | 1791906620 | ai-system-20261016-001 |

---

## 六、歷史歸屬（已被取代）

| 檔案 | 舊版本 | 舊 Writer | 新 Writer | 取代時間 |
|---|---|---|---|---|
| C-02-rules.md | 1791907900 | ai-system-20261016-001 | 1791908400 | 2026-10-16 |
| C-04-delivery.md | 1791907500 | ai-system-20261016-001 | 1791908500 | 2026-10-16 |

---

## 七、使用方式

### AI 生成編號流程

| 步驟 | 動作 |
|---|---|
| 1 | 使用者選擇專案 |
| 2 | 讀 PROJECT-LIST.md 取該專案 `code` |
| 3 | 讀本檔 §四 找該專案最新序號，+1 |
| 4 | 生成編號（如 webapp-20261016-001） |
| 5 | 每次回覆標：🆔 {編號} #{序號} |

### 每次回覆開頭格式

> 🆔 {對話編號} #{回覆序號}
> 📂 所屬專案：{專案顯示名稱}（第 {N} 個對話）

### Repo 識別流程

| 步驟 | 動作 |
|---|---|
| 1 | 讀本檔 §三之一 |
| 2 | 找對應 repo |
| 3 | 用實際名稱（不用代稱） |

---

## 八、維護規則

| 時機 | 動作 |
|---|---|
| 每次交付 | AI 更新 §五（現役） |
| 舊版被取代 | AI 移入 §六（歷史） |
| 新專案成立 | AI 更新 §三 |
| 新 Repo 成立 | AI 更新 §三之一 |
| 新對話建立 | AI 更新 §四 |
| 批次結束 | AI 輸出完整檔 |

**舊紀錄不刪除**：保留審計軌跡。

---

## 九、關聯檔案

| 主題 | 檔案 |
|---|---|
| 啟動卡 | C-00-startup.md |
| 通用規則 | C-02-rules.md |
| 交付格式 | C-04-delivery.md |
| 共同語言表 | C-11-terms.md |
| 專案清單 | PROJECT-LIST.md |
| 任務進度 | PROGRESS.md |

---

/* ═══ EOF ═══
F: AI-General/docs/records/R-01-writers.md
V: 1791910000
B: B34-4
W: ai-system-20261016-002
═══ */