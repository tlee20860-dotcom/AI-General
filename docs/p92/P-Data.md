# P-Data (p92 UPGRADE-WO)

**最後更新時間**: 2026-10-28
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
  | `salesReps` | array | 銷售員名稱陣列。 |
  | `uploadDate` | string | 建立/匯入日期（格式 `YYYY-MM-DD`）。 |
  | `dueDate` | string | 交貨日期（格式 `YYYY-MM-DD`，預設為空字串）。 |
  | `statusUpdateDate`| string | 最後一次更新狀態的日期時間（ISO 格式）。 |
  | `data` | object | **動態欄位容器**。存放所有自訂欄位（如金額、類別、客戶名稱等）。 |

### 2. `settings`（系統設定）
存放全站的動態配置，主要讀取 `settings/main` 這份文件。
- **資料結構**：
  | 欄位名稱 | 型態 | 說明 |
  |---|---|---|
  | `statuses` | array | 系統工序清單（例如：`["排產中", "印刷", "裁切"]`）。 |
  | `sales_mapping`| array | 銷售員對照表（物件陣列：`{ name: "王小明", aliases: ["123"] }`）。 |
  | `users` | array | 系統帳號清單（物件陣列：`{ username: "admin", password: "123456", role: "admin" }`）。 |
  | `schema` | array | **動態欄位定義**（物件陣列：`{ key: "amount", label: "金額", isSystem: false }`）。 |
  | `view_configs` | object | **視圖配置**。記錄每個頁面要顯示的欄位 `key`（例如：`{ kanban: ["id", "status"], table: ["id", "amount"] }`）。 |

---

## 二、動態 Schema 機制

這是本專案最重要的架構。舊版的 Firestore 資料是扁平的（所有欄位都在最外層），現在改為「核心欄位在外層，業務欄位在 `data` 內」。

### 如何新增欄位？
1. 使用者在「系統設定 ➜ 欄位管理」新增欄位。
2. 系統自動生成 `key`（如 `field_123`），並存入 `settings.schema`。
3. Excel 匯入時，`parser.js` 會根據 `schema` 的標題動態抓取資料，並存入 `work_orders/{id}.data` 中。
4. 若要在前端顯示，只需在「系統設定 ➜ 視圖配置」打勾即可。

### 注意事項
- **絕對不要**在程式碼中寫死 `order.data.amount` 或 `order.customerName`。若需取值，請使用 `order.data[key]`，並做好 `undefined` 的防呆。
- 核心欄位（如 `status`、`dueDate`）保留在最外層，不可放入 `data` 中。

/* ═══ EOF ═══
F: AI-General/docs/p92/P-Data.md
V: 1792915500
W: UPGRADE-002
═══ */