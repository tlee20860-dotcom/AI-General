# P-Architecture (p92 UPGRADE-WO)

**最後更新時間**: 2026-10-28
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

---

## 二、關鍵機制說明

### 1. 全域事件委派（Event Delegation）
為了徹底解決「切換頁面後按鈕點不到」的靈異現象，`order-view.js` 將點擊與輸入事件綁定在 `document` 上，並透過 `data-action` 與 `data-filter` 屬性來辨識目標。
- 切換視圖：`data-action="switch-view"`
- 排序：`th[data-sort]`
- 刪除：`data-action="delete"`
- 變更狀態：`select[data-action="change-status"]`

### 2. 資料清洗與日期防呆
- **星號過濾**：資料庫中若有 `*** 客戶查看中心` 這種垃圾資料，`order-view.js` 會在渲染前自動攔截剔除。
- **日期格式**：若讀取到 Excel 序列號（如 `46300`），會自動轉換為 `YYYY-MM-DD` 格式。

---

## 三、未來重構待辦（技術債）

1. **`settings.js` 體積過大（約 600 行）**：
   - 目前包含狀態、對照表、欄位、視圖配置等 7 個頁籤，已達 `W-03` 規範上限（800行）的警戒線。
   - **未來若需擴充新功能（如自訂選單名稱）**，必須將 `settings.js` 拆分為 `src/pages/settings/` 目錄下的子模組（如 `status-tab.js`、`schema-tab.js`），再由主檔動態載入，切勿繼續無腦擴充。
2. **PWA 與安全規則**：
   - PWA 已實作：`public/manifest.json`、`public/sw.js` 與 `src/engine/main.js` 的註冊邏輯均已完成，支援「加入主畫面」與離線快取。
   - 待補：`public/icons/icon-192.png` 與 `icon-512.png` 尚未上傳，缺圖會導致安裝失敗（見 W-04 §五）。
   - Firestore 安全規則目前為測試模式（`allow read, write: if true;`），上線前必須替換為 Firebase Auth 驗證。

/* ═══ EOF ═══
F: AI-General/docs/p92/P-Architecture.md
V: 1792918500
W: UPGRADE-004
═══ */