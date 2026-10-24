# 90-P-Rules（專案業務術語與專屬防呆）

用途：記錄本專案特有的業務術語與專屬操作規範。
說明：通用 Web App SOP 請見 `W-06`，通用 UI 結構請見 `W-05`。

---

## 一、專案業務術語

### 1.1 保險類
| 術語 | 說明 |
|---|---|
| 基金保險 | 投資型保險 |
| 普通保險 | 住院 / 人壽 / 意外 |
| 供滿 | 保單供款年期結束 |
| 平攤 | 將年繳保費按 12 個月分攤 |
| 代墊 | 成員先墊付保費 |
| 保單持有人 | policyHolderId |
| 受保人 | memberId |
| 供款期 | periodIndex |

### 1.2 收支類
| 術語 | 說明 |
|---|---|
| 家用轉入 | income 節點 |
| 個人收入 | personal_income 節點 |
| 共同支出 | memberId = 'shared' |
| 額外收入 | extra 節點 |

### 1.3 結算與基金類
| 術語 | 說明 |
|---|---|
| 待處理 | pending |
| 已處理 | done |
| 不適用 | skipped |
| 結算清單 | 整合個人支出 / 共同支出 / 保險扣款 |
| 保險基金 | type = 'insurance' |
| 獨立基金 | type = 'standalone' |
| 快照 | 每月記錄 |
| 累積供款 | cumulativeCost |
| 盈虧 | 現值 − 累積供款 |

### 1.4 銀行與角色類
| 術語 | 說明 |
|---|---|
| 家庭帳號 | type = 'family' |
| 個人帳號 | type = 'personal' |
| 初始餘額 | initialBalance |
| 銀行交易 | in / out / transfer |
| superadmin | 超級管理員 |
| owner | 家庭擁有者 |
| member | 家庭成員 |

---

## 二、專案專屬 SOP 與防呆

> 以下步驟為本專案 129 檔架構特有之操作，通用流程請見 `W-06-sop.md`。

### 2.1 新增頁面專屬步驟（結合 W-06 §一）
1. 遵循 W-06 通用步驟（寫 `js/pages`、`html`、更新 `sw.js`）
2. **更新 `js/config/constants.js` 的 `SIDEBAR_GROUPS` / `ROUTES`**
3. 更新 `90-P-Map.md` 的頁面區塊規格
4. 更新 `WF-STATE-INDEX` + `WF-PROGRESS`

### 2.2 改 Registry 專屬防呆
1. 讀 `90-P-Data.md`（資料結構）
2. grep 使用檔案（全域搜尋）
3. 加新 API（不破壞舊）
4. 改 registry
5. 更新文件 + WF-STATE-INDEX

**禁止**：改 export 名 / 改回傳格式 / 刪 export。

### 2.3 改 Functions API 專屬步驟（結合 W-02）
1. 讀 `90-P-Data.md` + `W-02`
2. 決定哪個 `_xxx.js`
3. 改 handler
4. 若加新端點 → 改 `[[path]].js` 分派
5. 更新文件 + WF-STATE-INDEX

**禁止**：新增獨立 `xxx.js` / 用 shim re-export。

### 2.4 變更影響矩陣

| 改動 | 同步更新 |
|---|---|
| 新增頁面 | WF-STATE-INDEX / WF-PROGRESS / 90-P-Map / sw.js / constants.js |
| 改 API | 90-P-Data / WF-STATE-INDEX |
| 改資料結構 | 90-P-Data |
| 修 Bug | 90-P-Errors / WF-PROGRESS / WF-STATE-INDEX |
| 改 Web App 通用 | W-* |

---

## 三、關聯檔案

| 主題 | 檔案 |
|---|---|
| 通用 SOP | `W-06-sop.md` |
| 通用 UI 結構 | `W-05-schema.md` |
| 專案架構 | `90-P-Map.md` |
| 資料結構 | `90-P-Data.md` |
| 歷史踩坑 | `90-P-Errors.md` |

/* ═══ EOF ═══
F: AI-General/docs/p90/90-P-Rules.md
V: 1792900062
W: ai-system-20261024-012#87
═══ */