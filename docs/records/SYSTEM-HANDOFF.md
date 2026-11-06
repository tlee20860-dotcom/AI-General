# SYSTEM-HANDOFF（體系交接快照）

上限：80 行
用途：體系層對話交接快照

version: SV14
records_pending: []

---

## 一、當前會話摘要

| 欄位 | 值 |
|---|---|
| 對話編號 | ai-system-009 |
| 本次範圍 | 實作偽 EOF 提取法、前端重命名刪除功能、廢除 P-* 統一為 WF-*，並確立 7 寶對稱架構。後期全面廢除雙軌制（增量與替換），強制單軌完整檔，並將前端拆分為雙版面。 |
| 累計回覆 | 約 80 次 |
| 狀態 | 準備進行 STATE_SEAL 重置 |

---

## 二、體系重大變更（SV14 二次重構）

1. **全面單軌制**：徹底廢除 `APPEND_ONLY` 與 `PARTIAL_REPLACE`。所有修改一律必須使用 `FULL_FILE`（完整檔），從物理層面根絕拼接斷裂與歷史檔污染。
2. **WF 命名大一統**：全面廢除專案 `P-*` 與數字前綴，統一為 `WF-*`（如 `WF-DATA.md`）。`setup-structure.yml` 與相關正則同步更新，並保留過渡期相容 `*P-*.md` 的抓取。
3. **專案 7 寶對稱**：專案結束 SOP 全面對齊體系，強制維護 7 個核心檔案（`WF-HANDOFF`、`WF-PROGRESS`、`WF-CONCLUSION`、`WF-EVOLUTION`、`WF-REJECTED`、`WF-DEBT`、`WF-ARCHIVE`）。
4. **歷史自動彙整**：`24-HISTORY.md` 打包時，除了體系歷史，還會自動掃描並合併所有專案的 `WF-EVOLUTION.md`。
5. **前端雙版面重構**：`index.html` 拆分為「常規發布 (FULL)」與「重命名發布 (RENAME)」雙版面。後者支援填寫舊路徑，發布新檔後自動呼叫 API 刪除舊檔，並具備物理阻斷防毀檔功能。

---

## 三、重建條件（下一 AI 優先確認）

| # | 優先確認 |
|---|---|
| 1 | 確認收到新四檔與狀態包（版本應為 SV14）。 |
| 2 | 確認前端控制台 `index.html` 已拆分為雙版面，並移除了增量與替換分頁。 |
| 3 | 檢查 `records_pending` 是否為空。 |
| 4 | **下一個體系對話編號為：`ai-system-010`**。 |

---

## 四、未完成事項（records_pending）

| 項目 | 狀態 |
|---|---|
| 無 | 全數處理完畢 |

---

## 五、下一步建議

| 順序 | 動作 |
|---|---|
| 1 | 將本次交接紀錄與更新之規則檔貼回 GitHub。 |
| 2 | 至 `AI-infra` 手動執行 `setup-structure.yml` 打包。 |
| 3 | 下載新合成物，確認 `20-SP-Sys.md` 版本為 `SV14`。 |
| 4 | 開啟新對話（ai-system-010），或進入專案對話執行 `P-*` 轉 `WF-*` 的重命名任務。 |

/* ═══ EOF ═══
F: AI-General/docs/records/SYSTEM-HANDOFF.md
V: 1793955000
W: ai-system-009
═══ */