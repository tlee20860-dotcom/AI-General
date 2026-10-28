# P-Dev-SOP (p92 UPGRADE-WO)

**最後更新時間**: 2026-10-28
**用途**: 專案開發 SOP，記錄如何在現有架構下擴充新功能（給下一個接手的 AI 或開發者）。

---

## 一、如何新增一個全新頁面？

由於本專案已導入「完全數據驅動」架構，新增頁面非常簡單，只需完成以下 4 個步驟，**絕對不要從頭手寫 HTML 表格**。

### 步驟 1：建立頁面檔案
在 `src/pages/` 目錄下建立新的檔案（例如 `newpage.js`），並參考現有的 `table.js` 結構。
- 必須匯出 `export default { async render() {...}, destroy() {...} }`。
- 在 `render()` 中讀取 `settings` 取得 `schema` 與 `view_configs`。
- 呼叫 `renderOrderView()` 來渲染資料，傳入 `pageKey: 'newpage'`。

### 步驟 2：註冊路由
打開 `src/engine/router.js`：
1. 在頂部 `import` 新的頁面（例如 `import NewPage from '../pages/newpage.js';`）。
2. 在 `routes` 物件中加入 `newpage: NewPage`。

### 步驟 3：新增側邊欄選單
打開 `src/ui/layout.js`：
1. 找到 `renderNavItems` 函式。
2. 在 `routes` 陣列中新增一個物件：
   `{ id: 'newpage', label: '新頁面名稱', icon: 'file-text', roles: ['admin', 'user'] }`。
3. 確保頂部 `import` 有引入對應的 Lucide 圖示（如 `FileText`）。

### 步驟 4：更新系統設定預設值
打開 `src/pages/settings.js`：
1. 在 `getDefaultViewConfigs()` 中，新增該頁面的預設顯示欄位（例如 `newpage: ['id', 'status']`）。
2. 在 `renderViewConfig()` 的 `pages` 陣列中，加入該頁面的標籤（例如 `{ key: 'newpage', label: '新頁面名稱', icon: 'file-text' }`），這樣使用者才能在設定中勾選欄位。

---

## 二、如何修改現有頁面的資料過濾邏輯？

**禁止**在頁面中直接操作 DOM。
請在頁面的 `updateUI()` 函式中，先對 `currentOrders` 進行 `filter` 或 `sort`，然後將過濾後的陣列傳給 `renderOrderView()`。`renderOrderView` 會自動處理後續的渲染。

---

## 三、如何新增動態欄位？

1. 使用者至「系統設定 ➜ 欄位管理」新增欄位。
2. 系統會自動生成 `key` 並存入 `settings.schema`。
3. 使用者至「系統設定 ➜ 視圖配置」勾選該欄位。
4. 匯入包含該欄位標題的 Excel，`parser.js` 會自動抓取並存入 `work_orders.data`。

**開發者完全不需要寫任何程式碼。**

/* ═══ EOF ═══
F: AI-General/docs/p92/P-Dev-SOP.md
V: 1792915600
W: UPGRADE-002
═══ */