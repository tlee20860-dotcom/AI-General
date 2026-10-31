# P-Architecture (p92 UPGRADE-WO)

**最後更新時間**: 2026-10-31
**用途**: 專案架構鐵律與防呆說明（給下一個接手的 AI 或開發者）。

---

## 一、核心架構原則：完全數據驅動（Data-Driven）

本專案經歷過重大重構，**已徹底廢除寫死欄位與手寫 HTML 表格/卡片的舊做法**。接手者必須嚴格遵守以下鐵律，否則將導致全站 UI 崩潰或功能失效。

### 1. 唯一大腦：`src/ui/order-view.js`
- **所有**頁面的工單顯示（卡片、表格、排序、篩選）皆由 `renderOrderView()` 統一渲染。
- **禁止**在任何 `src/pages/*.js` 中手寫 `<table>` 或 `<div class="glass-card">` 的 HTML 字串。
- **禁止**在各頁面中使用 `addEventListener` 綁定按鈕，**必須**使用 `order-view.js` 內建的全域事件委派（透過 `data-action` 屬性）。

### 2. 嚴禁寫死欄位（防硬編碼）
- 各頁面透過 `settings.view_configs[pageKey]` 取得要顯示的欄位，並傳入 `renderOrderView` 的 `visibleFields` 參數。
- 卡片與表格會自動根據 `visibleFields` 動態生成，**程式碼中不應再出現特定的業務欄位名稱**（如 `order.amount`），除非是透過 `getOrderValue` 取得的通用欄位。

### 3. 多角色權限三層防護
專案具備 `admin`、`worker`、`sales`、`viewer` 四種角色，權限控管分為三層：
- **路由層 (`engine/router.js`)**：攔截未授權的網址跳轉，強制重導向至該角色首頁。
- **UI 層 (`ui/layout.js`)**：側邊欄與頂部導覽列依據 `role` 隱藏無權限的選單。
- **渲染層 (`ui/order-view.js`)**：接收 `isReadOnly`（全部唯讀）與 `allowStatusChange`（僅允許按上下步）參數，精準控制各角色能操作的按鈕。

### 4. 彈窗模組化與三層架構
- 所有彈窗採用「標題固定、內容滾動、底部按鈕固定」的標準架構（`src/ui/modal.js`）。
- 複雜業務邏輯已抽離為獨立模組：
  - `src/ui/order-detail-modal.js`：負責工單詳細資料（交期、流程切換、進度推進）。
  - `src/ui/route-builder.js`：負責生產流程的快速新增與編輯。
- **禁止**在頁面層級各自實作輸入框的儲存或流程編輯邏輯。

---

## 二、關鍵機制說明

### 1. 全域事件委派與行內編輯
- `order-view.js` 將點擊與輸入事件綁定在 `document` 上，透過 `data-action` 辨識目標。
- 行內編輯（`isEditable` 欄位）在變更時，會拋出 `inline-edit` 自訂事件，由 `order-view-editor.js` 統一攔截並寫入資料庫，確保 UI 層不直接依賴資料層。

### 2. SortableJS 行動端拖曳
- 由於原生 HTML5 拖曳在手機端會與頁面滾動衝突，專案全面引入 `SortableJS`。
- 在設定頁的流程、區域、狀態排序，皆須設定 `forceFallback: true` 與 `fallbackTolerance: 3`，確保跨裝置拖曳流暢。

### 3. 本機 Excel 自動同步 (File System Access API)
- 在 `kanban.js` 中實作。透過 `showDirectoryPicker` 綁定本機資料夾。
- 結合 `setInterval` 與 `window.focus` 事件輪詢，比對 `lastModified` 時間，發現更新即自動匯入。
- **限制**：僅限支援 API 的桌機版 Chrome/Edge，手機端隱藏此按鈕；重新整理網頁後需重新授權。

### 4. 原生瀏覽器推播 (Notification API)
- 在 `engine/main.js` 中實作。系統啟動時請求權限，並背景監聽 `work_orders`。
- 當工單狀態改變時，比對當前登入者的權限：
  - 生產員：比對該工單「新狀態」是否屬於其負責的區域。
  - 銷售員：比對該工單的銷售員是否在授權清單內。
- 若符合則觸發原生通知（網頁需保持在背景執行）。

### 5. 資料清洗與日期防呆
- **星號過濾**：資料庫中若有 `*** 客戶查看中心` 這種垃圾資料，`order-view.js` 會在渲染前自動攔截剔除。
- **日期格式**：若讀取到 Excel 序列號（如 `46300`），會自動轉換為 `YYYY-MM-DD` 格式。

---

## 三、未來重構待辦（技術債）

1. **Firebase Auth**：
   - Firestore 安全規則目前為測試模式（`allow read, write: if true;`），上線前必須替換為 Firebase Auth 驗證。
   - 目前帳密驗證為前端明文比對，需升級安全性。
2. **原生推播限制**：純前端 `Notification API` 僅在網頁未完全關閉時有效，若需「關閉網頁也能收到通知」，需日後引入 FCM 或 OneSignal。

/*
F: AI-General/docs/p92/P-Architecture.md
V: 1792989700
W: UPGRADE-006
*/