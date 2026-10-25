# WF-HANDOFF（專案交接快照）

上限：80 行（嚴格限制）
用途：提供下一輪對話 AI 的專案現況快照

---

## 一、當前會話摘要

| 欄位 | 值 |
|---|---|
| 對話編號 | ai-system-20261024-012 |
| 本次範圍 | 徹底重構新版（P0~P7），包含前端 SPA、模組化後端、UI 統一排版 |
| 狀態 | 核心重構已完成，等待最後排版套用與功能驗收 |

---

## 二、議題進度與重大變更

1. **架構重寫**：廢棄舊版 119 檔架構，採用 SPA（單頁應用）+ Hash 路由，將前端重組為 `engine`、`domain`、`ui`、`pages` 等模組（約 45 檔）。
2. **後端重構**：將舊版 11 個 API 檔整合為 5 檔（`config`, `helpers`, `handlers-core`, `handlers-report`, `handlers-admin`），並修正 Cloudflare Pages Functions 的目錄路徑至 `functions/api/`。
3. **資料層分離**：將舊版 1000 行的 `db.js` 拆分為 `read.js` 與 `write.js`，並實作 `?readonly=1` 防呆。
4. **UI 統一化**：建立 `renderPageLayout` 統一全站頁面骨架（標題 → 統計卡 → 控制列 → 列表），並支援表格/卡片切換。

---

## 三、重建條件（下一 AI 優先確認）

| # | 優先確認 |
|---|---|
| 1 | 確認 `engine/main.js` 與 `engine/router.js` 的登入跳轉與事件綁定邏輯是否正確。 |
| 2 | 確認 `ui/layout.js` 的 `renderPageLayout` 是否已正確匯出。 |
| 3 | 確認 `pages/insurance.js` 已補齊完整的 Modal 與刪除邏輯。 |

---

## 四、未完成事項（待 Ken 執行或下一階段處理）

| 項目 | 狀態 |
|---|---|
| 套用統一排版至剩餘頁面 | `bank`, `settlements`, `code-list`, `member-report`, `portfolio` 需改寫為使用 `renderPageLayout`。 |
| 補齊 `input-center.js` 非支出 Tab 的列表 | 目前切換到保險/基金/銀行時，僅顯示提示字，未渲染實際清單。 |
| 全面功能測試 | 測試新增/編輯/刪除是否能正確寫入 Firebase。 |

---

## 五、下一步建議

| 順序 | 動作 |
|---|---|
| 1 | 將剩餘頁面的 `content.innerHTML` 手寫排版，替換為 `renderPageLayout` 呼叫。 |
| 2 | 實作 `input-center` 中其他 Tab（保險、基金、銀行）的清單渲染。 |
| 3 | 測試新增保單、新增支出、結算確認扣款等核心流程。 |

/* ═══ EOF ═══
F: AI-General/docs/p90/WF-HANDOFF.md
V: 1792900940
W: ai-system-20261024-012#86
═══ */