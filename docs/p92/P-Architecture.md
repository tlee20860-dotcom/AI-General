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

### 3. 單一編輯入口（Modal）
- 列表頁（總表、類別、銷售員）**禁止**提供行內編輯或下拉選單修改資料。
- 所有修改**必須**點擊單號，開啟 `openOrderModal` 進行編輯。
- 唯一例外是「工單進度表（看板）」，保留上下步按鈕以利現場推進度。
- 彈窗採用三層架構（標題固定、內容滾動、底部按鈕固定），確保手機端也能完美操作。

### 4. 表單引擎與純函數分離
- **工單編輯器（`order-editor.js`）**：負責根據 `schema` 渲染輸入框、製程路線圖、外發供應商與物料明細。不直接處理寫入邏輯。
- **公式計算（`formula-engine.js`）**：為純函數，負責解析 `{{欄位}}` 並回傳計算結果。
- **差異核對（`data-diff.js`）**：為純函數，負責比對兩筆資料的差異，回傳差異物件供 UI 標示。

### 5. 資料防護與全量更新（極重要）
- **禁止使用 `setDocument` 覆蓋 `settings/main`**。這會導致未被包含的欄位（如區域、模板、物料）被全部洗掉。
- **所有設定儲存必須使用 `updateDocument`**，且只傳入當下修改的欄位（如僅傳入 `materials` 或 `suppliers`）。

### 6. 四大設定中心
- **工單管理設定（`settings-form.js`）**：表單佈局、欄位管理、視圖配置、頁面管理、公式設定、核對清單。
- **生產管理設定（`settings.js`）**：狀態、類別、製程路線圖、區域、區域狀態、對照表、外發供應商。
- **物料管理設定（`settings-material.js`）**：物料主檔、自訂欄位、詳細資料。
- **系統管理設定（`settings-system.js`）**：帳號管理、資料管理。

---

## 二、關鍵機制說明

### 1. 全域事件委派（Event Delegation）
為了解決「切換頁面後按鈕點不到」的現象，`order-view.js` 將事件綁定在 `document` 上，並透過 `data-action` 與 `data-filter` 屬性來辨識目標。

### 2. 資料清洗與日期防呆
- **星號過濾**：資料庫中若有 `*** 客戶查看中心` 等垃圾資料，`order-view.js` 會在渲染前自動攔截剔除。
- **日期格式**：若讀取到 Excel 序列號（如 `46300`），會自動轉換為 `YYYY-MM-DD` 格式。

### 3. 全域設定即時監聽
- `src/engine/main.js` 啟動時會監聽 `settings/main`，當系統設定變更時，會派發 `settings-updated` 與 `nav-config-updated` 事件。
- 各前台頁面收到事件後會自動刷新畫面，不需手動重新整理。

### 4. 匯入防覆寫與備份還原
- **日常匯入**：針對已存在的工單，僅更新 Excel 來源欄位與開單日期，保留手動修改的狀態與交期。
- **備份還原**：若匯入的 Excel 包含「狀態」與「製程路線」，且該工單在系統中不存在，則會直接套用 Excel 的狀態與路線建立新單。
- **自動偵測表頭**：`parser.js` 會掃描前 20 行尋找「單號」或「登錄」等關鍵字，不強制表頭在第一行。
- **多檔案同步**：`kanban.js` 使用 `localStorage` 記錄各檔案的修改時間，支援多個不同檔名的 Excel 獨立追蹤。
- **類別自動補齊**：匯入時若發現新類別，會自動寫入 `settings.categories`。

### 5. 物料與外發供應商
- 物料與供應商皆為獨立主檔（`settings.materials`、`settings.suppliers`），支援自訂欄位（`material_schema`、`supplier_schema`）。
- 工單編輯時，物料下拉選單會依工單類別過濾（`m.categories.includes(orderCategory)`）。
- 工單儲存時，會將物料明細存入 `work_orders.materials`，將外發商存入 `work_orders.supplierName`。

---

## 三、未來重構待辦（技術債）

1. **表單佈局切換未完全實作**：
   - `settings-form.js` 已可設定 A/B/C 三種佈局，但 `order-editor.js` 目前僅實作平鋪模式（A）。
   - 需補齊模式 B（分頁）與模式 C（左右對照）的渲染邏輯。
2. **W 包已同步**：
   - 本次實作經驗已沉澱至 W 包：單一編輯入口見 `W-03`；多檔案同步與表頭偵測見 `W-06`；全量覆蓋防呆與類別自動同步見 `W-07`。
3. **Firebase Auth**：
   - Firestore 安全規則目前為測試模式（`allow read, write: if true;`），上線前必須替換為 Firebase Auth 驗證。
   - 目前帳密驗證為前端明文比對，需升級安全性。

/* ═══ EOF ═══
F: AI-General/docs/p92/P-Architecture.md
V: 1793074000
W: UPGRADE-007
═══ */