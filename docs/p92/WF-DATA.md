# WF-DATA (p92 UPGRADE-WO)

<!-- === 關聯規則防呆矩陣 ===
| 本次修改項 | 命中關聯條文 | 具體防呆約束／隔離措施 | 檢核結果 |
| 技術檔更名 P-Data.md ➜ WF-DATA.md | R-024、F-010 | 舊路徑已於交付清單獨立列出，供控制台刪除 | PASS |
| 對齊 SV14 七寶架構 | A-00 §4.4、詞 101 | 檔名改為 WF-*，內容保留原技術說明 | PASS |
======================== -->

**最後更新時間**: 2026-11-09
**用途**: 定義 Firestore 資料庫結構與動態 Schema 機制（給下一個接手的 AI 或開發者）。

---

## 一、資料集（Collections）說明

本專案使用 Firebase Firestore 作為資料庫，主要包含兩個核心集合：

### 1. `work_orders`（工單資料集）
存放所有工單的即時狀態與資料。
- **文件 ID**：由 Excel 匯入的「工單號碼（發票）」作為主鍵（Document ID）。
- **資料結構**：
  | 欄位名稱 | 型態 | 說明 |
  |---|---|---|
  | `id` | string | 工單號碼（與 Document ID 相同，方便前端讀取）。 |
  | `status` | string | **生產進度（工序）**。對應 `settings.statuses` 的其中一個值。 |
  | `route` | array | 製程路線圖（工序名稱陣列）。若未設定則沿用 `settings.statuses`。 |
  | `salesReps` | array | 銷售員名稱陣列。 |
  | `supplierName` | string | 外發供應商名稱（對應 `settings.suppliers` 的 `name`）。 |
  | `materials` | array | 工單物料明細。每筆物件含 `materialId`、`name`、`qty`、`note`。 |
  | `uploadDate` | string | 開單日期（格式 `YYYY-MM-DD`）。 |
  | `dueDate` | string | 交貨日期（格式 `YYYY-MM-DD`，預設為空字串）。 |
  | `statusUpdateDate` | string | 最後一次更新狀態的日期時間（ISO 格式）。 |
  | `source` | string | 資料來源：`manual`（手動新增）或 `excel`（Excel 匯入）。 |
  | `diff` | object | 差異核對標記。若有差異，記錄各欄位的 `db`（手動值）與 `excel`（Excel 值）。 |
  | `data` | object | **動態欄位容器**。存放所有自訂欄位（如金額、類別、客戶名稱等）。 |

### 2. `settings`（系統設定）
存放全站的動態配置，主要讀取 `settings/main` 這份文件。
- **資料結構**：
  | 欄位名稱 | 型態 | 說明 |
  |---|---|---|
  | `statuses` | array | 系統工序清單（例如：`["排產中", "印刷", "裁切"]`）。 |
  | `categories` | array | 工單類別清單（例如：`["GF", "LS", "UG"]`）。 |
  | `sales_mapping` | array | 銷售員對照表（物件陣列：`{ name: "王小明", aliases: ["123"] }`）。 |
  | `users` | array | 系統帳號清單（物件陣列：`{ username: "admin", password: "123456", role: "admin", allowedAreas: [], allowedSales: [] }`）。 |
  | `schema` | array | **動態欄位定義**（物件陣列：`{ key: "amount", label: "金額", type: "number", isSystem: false, isEditable: true }`）。 |
  | `view_configs` | object | **視圖配置**。記錄每個頁面要顯示的欄位 `key`（例如：`{ kanban: ["id", "status"], table: ["id", "amount"] }`）。 |
  | `route_templates` | array | 製程路線模板（物件陣列：`{ name: "標準流程", categories: ["GF"], steps: ["印刷", "裁切"] }`）。 |
  | `areas` | array | 生產區域（物件陣列：`{ id, name, categories: [], allowedStatuses: [], statuses: [], currentStatus }`）。 |
  | `areaStatuses` | array | 區域狀態字典（例如：`["正常", "壞機", "休息中"]`）。 |
  | `materials` | array | 物料主檔（物件陣列：`{ id, name, categories: [], data: {} }`）。 |
  | `material_schema` | array | 物料自訂欄位定義（物件陣列：`{ key, label, type }`）。 |
  | `suppliers` | array | 外發供應商主檔（物件陣列：`{ id, name, data: {} }`）。 |
  | `supplier_schema` | array | 供應商自訂欄位定義（物件陣列：`{ key, label, type }`）。 |
  | `form_layout` | string | 表單佈局模式：`A`（平鋪）、`B`（分頁）、`C`（左右對照）。 |
  | `formulas` | object | 公式設定（物件：`{ targetKey: "{{quantity}} * {{price}}" }`）。 |
  | `diff_fields` | array | 差異核對欄位清單（例如：`["amount", "quantity"]`）。 |
  | `nav_config` | array | 側邊欄與頂部導覽配置（物件陣列）。 |

---

## 二、動態 Schema 機制

這是本專案最重要的架構。舊版的 Firestore 資料是扁平的（所有欄位都在最外層），現在改為「核心欄位在外層，業務欄位在 `data` 內」。

### 如何新增欄位？
1. 使用者在「工單管理設定 ➜ 欄位管理」新增欄位。
2. 系統自動生成 `key`（如 `field_123`），並存入 `settings.schema`。
3. Excel 匯入時，`parser.js` 會根據 `schema` 的標題動態抓取資料，並存入 `work_orders/{id}.data` 中。
4. 若要在前端顯示，只需在「工單管理設定 ➜ 視圖配置」打勾即可。

### 注意事項
- **絕對不要**在程式碼中寫死 `order.data.amount` 或 `order.customerName`。若需取值，請使用 `order.data[key]`，並做好 `undefined` 的防呆。
- 核心欄位（如 `status`、`dueDate`、`route`、`materials`、`supplierName`）保留在最外層，不可放入 `data` 中。

### 資料正規化
- `route` 欄位可能因舊資料或 Excel 匯入而為字串（以 `,` 或 `→` 分隔）。讀取時必須先以 `normalizeRoute` 函式統一轉為陣列，再進行比對。
- `salesReps` 為陣列；若讀到字串，需先轉為陣列。
- `materials` 為陣列；若讀到空值或非陣列，視為空明細。

### 全域搜尋支援物料（UPGRADE-008）
- `src/domain/global-search.js` 的 `flattenOrder` 會讀取 `work_orders.materials` 陣列。
- 每筆物料的 `name` 與 `note` 會展平為 `materials.{idx}.name` 與 `materials.{idx}.note`，納入關鍵字比對範圍。
- 因此，搜尋「110G」或「毛紙」等物料名稱片段，即可命中包含該物料的工單。

### SV14 對齊說明
- 本檔已由 `P-Data.md` 更名為 `WF-DATA.md`，與其他 `WF-*` 紀錄檔共構七寶對稱架構。
- 後續資料結構變更說明，統一寫入本檔，不再使用 `P-*` 命名。

/* ═══ EOF ═══
F: AI-General/docs/p92/WF-DATA.md
V: 1794184200
W: UPGRADE-008
═══ */