# 遷移使用說明

最後更新：A20261016-001
用途：說明如何執行一次性遷移，以及未來如何重複使用

---

## 一、第一次遷移（從 AI-training-files 到新架構）

### 前置作業

| # | 檢查項目 | 確認 |
|---|---|---|
| 1 | `AI-General` 倉庫已存在 | ☐ |
| 2 | `AI-General` 已放入 `MIGRATION.md` | ☐ |
| 3 | `AI-General` 已放入 `setup-migration.yml` | ☐ |
| 4 | `AI-General` 有 `CROSS_REPO_PAT` Secret（含 `repo` + `workflow` 權限） | ☐ |
| 5 | `WEB-APP-Family` 已由 `v2.Family` 改名完成 | ☐ |
| 6 | `AI-training-build` 已建立 | ☐ |

### 執行 phase-1（複製）

| 步驟 | 動作 |
|---|---|
| 1 | 進入 `AI-General` 的 **Actions** 分頁 |
| 2 | 左側選擇 **Setup Migration** |
| 3 | 點擊 **Run workflow** |
| 4 | `phase` 選擇 **phase-1** |
| 5 | 點擊綠色 **Run workflow** 按鈕 |
| 6 | 等待約 1 分鐘，確認綠色勾勾 ✅ |

### 驗證 phase-1

執行完成後，檢查以下項目：

| 倉庫 | 應出現的內容 |
|---|---|
| AI-General | `docs/common/C-*.md`、`docs/skills/W/W-*.md`、`docs/records/R-*.md`、`.github/workflows/setup-structure.yml` |
| WEB-APP-Family | `docs/projects/web-app-family/*.md` |

**確認無誤後，才執行 phase-2。**

### 執行 phase-2（刪除源頭）

| 步驟 | 動作 |
|---|---|
| 1 | 再次進入 **Actions** → **Setup Migration** |
| 2 | 點擊 **Run workflow** |
| 3 | `phase` 選擇 **phase-2** |
| 4 | 點擊綠色 **Run workflow** 按鈕 |
| 5 | 等待約 1 分鐘，確認綠色勾勾 ✅ |

執行完成後，`AI-training-files` 中的 C-*、W-*、R-*、P-*（family-fin）會被刪除。

---

## 二、未來架構變更時

當你需要再次調整倉庫架構時：

| 步驟 | 動作 |
|---|---|
| 1 | 修改 `MIGRATION.md`：更新「參與倉庫」清單、新增/修改/刪除「任務」區塊 |
| 2 | Commit `MIGRATION.md` |
| 3 | 手動觸發 `Setup Migration`，選擇 `phase-1` |
| 4 | 驗證無誤後，執行 `phase-2` |

**不需要修改 `setup-migration.yml`**，因為它會動態讀取 `MIGRATION.md`。

---

## 三、注意事項

| # | 注意事項 |
|---|---|
| 1 | phase-1 執行後，**務必先驗證**再執行 phase-2，避免檔案遺失 |
| 2 | `source_path` 支援 `*` 通配符，例如 `docs/common/C-*.md` |
| 3 | `target_path` 以 `/` 結尾代表目錄 |
| 4 | 如果來源或目標倉庫不存在，該任務會被跳過 |
| 5 | 所有 commit 都帶有 `[skip ci]`，不會觸發其他 Actions |
| 6 | 同一個倉庫如果同時是來源和目標，會正確處理 |

---

## 四、疑難排解

| 症狀 | 原因 | 解法 |
|---|---|---|
| clone 失敗 | PAT 權限不足 | 確認 `CROSS_REPO_PAT` 有 `repo` 權限 |
| push 失敗 | 目標倉庫無寫入權限 | 確認 PAT 有 `workflow` 權限 |
| 任務被跳過 | 來源或目標路徑不存在 | 檢查 `MIGRATION.md` 的路徑 |
| 檔案沒有搬過去 | 通配符沒展開 | 確認 `source_path` 結尾正確 |
| Actions 沒出現 Setup Migration | workflow 檔案沒放對位置 | 確認 `.github/workflows/setup-migration.yml` 存在 |

---

## 五、關聯檔案

| 主題 | 檔案 |
|---|---|
| 遷移清單 | MIGRATION.md |
| 遷移 Action | .github/workflows/setup-migration.yml |

---

/* ═══ EOF ═══
F: AI-General/MIGRATION-GUIDE.md
V: 1791906620
B: B34-4
W: A20261016-001
═══ */
