## 📄 AI-General/docs/p92/P-Architecture.md

# P-Architecture (p92 UPGRADE-WO)

**最後更新時間**: 2026-11-02
**用途**: 專案架構鐵律與防呆說明（給下一個接手的 AI 或開發者）。

---

## 一、核心架構原則：完全數據驅動（Data-Driven）

本專案經歷過重大重構，**已徹底廢除寫死欄位與手寫 HTML 表格/卡片的舊做法**。接手者必須嚴格遵守以下鐵律，否則將導致全站 UI 崩潰或功能失效。

### 1. 唯一大腦：`src/ui/order-view.js`
- **所有**頁面的工單顯示（卡片、表格、排序、篩選）皆由 `renderOrderView()` 統一渲染。
- **禁止**在任何 `src/pages/*.js` 中手寫 `<table>` 或 `<div class="glass-card">` 的 HTML 字串。
- **禁止**在各頁面中使用 `addEventListener` 綁定按鈕，**必須**使用 `order-view.js` 內建的全域事件委派（透過 `data-action` 屬性）。

### 2. 嚴禁寫死欄位（防硬編碼）
- 舊版程式碼曾寫死 `order.data.customerName`、`order.amount` 等欄位，這導致換一份 Excel 就必須改程式碼。
- **現在的做法**：各頁面透過 `settings.view_configs[pageKey]` 取得要顯示的欄位，並傳入 `renderOrderView` 的 `visibleFields` 參數。
- 卡片與表格會自動根據 `visibleFields` 動態生成，**程式碼中不應再出現特定的業務欄位名稱**。

### 3. 行內編輯（Inline Edit）
- 表格與卡片中，若欄位屬性 `isEditable` 為 `true`，`order-view.js` 會自動渲染成 `<input>`。
- 變更時透過全域事件派發 `inline-edit`，由 `order-view-editor.js` 統一攔截並寫入資料庫。
- **禁止**在頁面層級各自實作輸入框的儲存邏輯。

### 4. 彈窗三層架構（Modal）
- `src/ui/modal.js` 採用「標題固定、內容滾動、底部按鈕固定」的標準架構。
- 呼叫 `openModal` 時，若內容會超過螢幕高度，**必須**將按鈕 HTML 傳入 `footer` 參數，切勿將按鈕寫在 `content` 的最下方，以免在手機上被截斷。

### 5. 表單引擎與純函數分離
- **資料錄入（`data-entry.js`）**：僅負責頁面排版與資料載入。
- **表單渲染（`order-editor.js`）**：僅負責根據 `schema` 渲染輸入框與綁定事件。不直接處理寫入邏輯。
- **公式計算（`formula-engine.js`）**：為純函數，負責解析 `{{欄位}}` 並回傳計算結果，不碰 DOM 與 Firebase。
- **差異核對（`data-diff.js`）**：為純函數，負責比對兩筆資料的差異，回傳差異物件供 UI 標示。

### 6. 手動優先與差異核對
- 若工單來源為 `manual`，Excel 匯入時**絕對不可**覆蓋核心進度與金額。
- 差異標記（`order.diff`）會在 UI 上顯示為紅色驚嘆號，只有當使用者在介面上手動修改該欄位後，才會清除標記。

---

## 二、關鍵機制說明

### 1. 全域事件委派（Event Delegation）
為了徹底解決「切換頁面後按鈕點不到」的靈異現象，`order-view.js` 將點擊與輸入事件綁定在 `document` 上，並透過 `data-action` 與 `data-filter` 屬性來辨識目標。
- 切換視圖：`data-action="switch-view"`
- 排序：`th[data-sort]`
- 刪除：`data-action="delete"`
- 工序推進：`data-action="prev-step"` / `data-action="next-step"`

### 2. 資料清洗與日期防呆
- **星號過濾**：資料庫中若有 `*** 客戶查看中心` 這種垃圾資料，`order-view.js` 會在渲染前自動攔截剔除。
- **日期格式**：若讀取到 Excel 序列號（如 `46300`），會自動轉換為 `YYYY-MM-DD` 格式。

### 3. 全域設定即時監聽
- `src/engine/main.js` 啟動時會監聽 `settings/main`，當系統設定（如工序、模板）變更時，會派發 `settings-updated` 事件。
- 各前台頁面（`kanban`、`table` 等）收到事件後會自動刷新畫面，不需手動重新整理。

### 4. 匯入防覆寫與備份還原
- **日常匯入**：針對已存在的工單，僅更新 Excel 來源欄位（如銷售員、自訂欄位），保留手動修改的狀態與交期。
- **備份還原**：若匯入的 Excel 包含「狀態」與「製程路線」，且該工單在系統中不存在，則會直接套用 Excel 的狀態與路線建立新單。

### 5. 全域搜尋引擎
- `global-search.js` 會將工單物件攤平，進行跨欄位的關鍵字比對，並支援狀態、類別、日期的進階過濾。

---

## 三、未來重構待辦（技術債）

1. **表單佈局切換未完全實作**：
   - `settings-form.js` 已可設定 A/B/C 三種佈局，但 `order-editor.js` 目前僅實作平鋪模式。
   - 需補齊模式 B（分頁）與模式 C（左右對照）的渲染邏輯。
2. **體系 W 包已同步（2026-10-30 補記）**：
   - 本次實作經驗已沉澱至 W 包：三層 Modal 架構見 `W-05 §0.3`；全域即時監聽與行內編輯見 `W-03 §0.2`（`W03-R10`、`W03-R11`）；雙清單拖曳見 `W-06 §三`；PWA 圖示規範見 `W-04 §3.1`。原 `D-022`／`D-023` 已改派為 `D-239`／`D-240`，補記動作見 `D-241`。
3. **Firebase Auth**：
   - Firestore 安全規則目前為測試模式（`allow read, write: if true;`），上線前必須替換為 Firebase Auth 驗證。
   - 目前帳密驗證為前端明文比對，需升級安全性。

/* ═══ EOF ═══
F: AI-General/docs/p92/P-Architecture.md
V: 1793019000
W: UPGRADE-006
═══ */