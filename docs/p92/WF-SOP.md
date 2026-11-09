# WF-SOP (p92 UPGRADE-WO)

<!-- === 關聯規則防呆矩陣 ===
| 本次修改項 | 命中關聯條文 | 具體防呆約束／隔離措施 | 檢核結果 |
| 技術檔更名 P-Dev-SOP.md ➜ WF-SOP.md | R-024、F-010 | 舊路徑已於交付清單獨立列出，供控制台刪除 | PASS |
| 對齊 SV14 七寶架構 | A-00 §4.4、詞 101 | 檔名改為 WF-*，內容保留原技術說明 | PASS |
======================== -->

**最後更新時間**: 2026-11-09
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

1. 使用者至「工單管理設定 ➜ 欄位管理」新增欄位。
2. 系統會自動生成 `key` 並存入 `settings.schema`。
3. 使用者至「工單管理設定 ➜ 視圖配置」勾選該欄位。
4. 匯入包含該欄位標題的 Excel，`parser.js` 會自動抓取並存入 `work_orders.data`。

**開發者完全不需要寫任何程式碼。**

---

## 四、如何新增物料或外發供應商？

### 物料
1. 使用者至「物料管理設定」新增物料，可設定適用類別與自訂欄位。
2. 工單編輯彈窗中，物料下拉選單會依工單類別過濾（`m.categories.includes(orderCategory)`）。
3. 儲存時，物料明細存入 `work_orders.materials`（陣列，每筆含 `materialId`、`name`、`qty`、`note`）。

### 外發供應商
1. 使用者至「生產管理設定 ➜ 外發供應商」新增供應商，可設定自訂欄位。
2. 工單編輯彈窗中，外發供應商下拉選單讀取 `settings.suppliers`。
3. 儲存時，供應商名稱存入 `work_orders.supplierName`（字串）。

---

## 五、如何讓新欄位可被全域搜尋？

### 一般動態欄位（`data` 內）
- 只要欄位存在於 `work_orders.data` 中，`global-search.js` 的 `flattenOrder` 會自動將其展平為 `data.{key}`，無需額外修改程式碼。

### 陣列型欄位（如 `materials`）
- 若為陣列結構（如工單物料），需在 `flattenOrder` 中額外處理。
- 範例：`materials` 陣列的處理方式為，將每筆物料的 `name` 與 `note` 展平為 `materials.{idx}.name` 與 `materials.{idx}.note`。
- 新增類似陣列欄位時，請依此模式在 `flattenOrder` 中補上對應的展平邏輯，並確保不將整個物件轉為 `[object Object]`。

---

## 六、SV14 對齊說明

- 本檔已由 `P-Dev-SOP.md` 更名為 `WF-SOP.md`，與 `WF-HANDOFF`、`WF-PROGRESS`、`WF-CONCLUSION`、`WF-EVOLUTION`、`WF-REJECTED`、`WF-DEBT`、`WF-ARCHIVE`、`WF-ARCH`、`WF-DATA` 共構 SV14 七寶對稱架構。
- 後續開發 SOP 的補充與修訂，統一寫入本檔，不再使用 `P-*` 命名。
- 舊檔 `P-Dev-SOP.md` 由控制台刪除；舊路徑已於交付清單獨立列出（見 `~~~text` 區塊）。

/* ═══ EOF ═══
F: AI-General/docs/p92/WF-SOP.md
V: 1794184300
W: UPGRADE-008
═══ */