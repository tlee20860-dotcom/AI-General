# 90-P-Errors（專案歷史與踩坑精華）

用途：記錄本專案特有的事故與決策，防止 AI 重蹈覆轍。
說明：通用錯誤防呆請見 `W-07-errors.md`。此處僅保留專案專屬的致命災難與業務決策。

---

## 一、重大歷史決策（精華）

> 完整 ADR 與歷史決策已濃縮，此處僅列對專案架構影響最深遠的決策。

| 編號 | 決策 | 說明 |
|---|---|---|
| D-063 | entity-create 單一端點 | 廢棄所有獨立 CRUD 端點，統一由 `POST /api/entity-create` 處理（含 action 參數）。 |
| D-118 | 通用大腦 + N 領域技能包 | 將通用邏輯抽離至體系 W 包（W-00~W-07）。 |
| D-170 | SPA 重構與後端合併 | 前端 129 檔合併為 11 檔，後端 11 檔合併為 2 檔（已廢棄）。 |
| D-173 | 廢棄巨型 SPA 改回模組化 | 解決 AI 截斷與遺漏問題，改回模組化架構並採用純函數渲染。 |
| D-175 | V2 全新架構與清空重建 | 放棄漸進式修改，直接清空重寫，分離前後端目錄。 |

---

## 二、專案專屬致命踩坑（Top 7）

### 2.1 P-32：V2 登入狀態白屏與無限迴圈
*   **症狀**：使用者登入後，畫面全黑，或卡在登入頁無限重載。
*   **原因**：`main.js` 在 `lookup-family` 失敗時直接執行 `signOut(auth)` 並清空 `app-root`，導致 `onAuthStateChanged` 觸發時找不到 DOM 容器渲染登入頁。
*   **正確做法**：保留主骨架，當 `lookup-family` 失敗時顯示 Toast 並交由 `router.js` 導向登入頁，且確保登入頁能正確隱藏側邊欄。

### 2.2 P-33：表格手機版斷行與擠壓
*   **症狀**：在手機端，表格的數字（如 `HK$ 139,692`）換行，或「今年」標籤被擠成直排。
*   **原因**：`ui/table.js` 未對 `td` 加上 `white-space: nowrap`，且未設定表格的 `min-width` 導致過度擠壓。
*   **正確做法**：表格加上 `min-width: 600px` 與 `overflow-x: auto`，並在 `th`, `td` 加上 `white-space: nowrap`，允許橫向滑動。

### 2.3 B31-1：狀態覆蓋與快取失效
*   **症狀**：已供款資訊不刷新；換家庭後狀態解析錯誤。
*   **原因**：`_lastIds` id 快取擋住 `insurance_payments` 更新；`merge.js` 模組級快取未監聽 family-change。
*   **正確做法**：需訂閱 `insurance_payments`；加 `AppState.on('family-change')`。

### 2.4 B30-8：基金成本計算錯誤
*   **症狀**：四支基金投入成本皆顯示相同數字，總計錯誤。
*   **原因**：`_resolveCost` 未乘以該基金在保單中的比例（pct）；手動輸入成本的基金比例為 0。
*   **正確做法**：修正 `_resolveCost`：先扣除手動成本，剩餘按比例分配。

### 2.5 B30-5：後端永遠連舊 DB
*   **症狀**：superadmin 登入新 DB 後，API 顯示「需要超級管理員權限」。
*   **原因**：`_config.js` 寫死舊 DB URL；CF Pages 不支援 `process.env`；移除 FIREBASE_DB_URL export 導致崩潰。
*   **正確做法**：CF Pages env 走 `handler { env }`；不得移除既有 export，改用 `export let + initConfig`。

### 2.6 上傳檔案失誤：覆蓋與未 Push
*   **症狀**：修改基金成本後畫面數字未變。
*   **原因**：手動修改時把 `insurance.js` 貼到了 `portfolio.js`；只 Commit 未 Push。
*   **正確做法**：推送前必須逐一核對「檔名 ↔ 內容」。

### 2.7 早期 UI 與年月切換災難
*   **症狀**：多頁缺 view toggle、換年月不重整、已供滿保單不能展開。
*   **原因**：`page-controls.js` 的 year/month 值在 `customMount` 快照一次；`insurance.js` 遺漏展開 handler。
*   **正確做法**：動態值必須內部讀取 `AppState`；新頁面必須手動初始化 `initViewToggle`。

---

## 三、專案專屬交付前防呆清單

| # | 類型 | 防止做法 |
|---|---|---|
| 1 | API 路徑錯誤 | 確認 API 檔案是否放在 `functions/api/`，而非根目錄 `api/`。 |
| 2 | 路由事件傳參 | 確認 `addEventListener` 是否有正確包裝箭頭函式，避免 Event 物件污染參數。 |
| 3 | UI 狀態不同步 | 切換按鈕點擊時，需同時更新底層狀態（如 `AppState`）與按鈕的視覺樣式。 |
| 4 | 數據源語意不符 | 年度報表確認使用年度 API，勿使用單月 API 替代。 |
| 5 | 檔案貼錯 | 手動貼上 GitHub 前，確認檔名與內容相符。 |

---

## 四、關聯檔案

| 主題 | 檔案 |
|---|---|
| 專案架構 | `90-P-Map.md` |
| 資料結構 | `90-P-Data.md` |
| 專案業務與防呆 | `90-P-Rules.md` |
| 通用錯誤防呆 | `W-07-errors.md` |
| 體系學習日誌 | `R-04-learning.md` |

/* ═══ EOF ═══
F: AI-General/docs/p90/90-P-Errors.md
V: 1792900127
W: ai-system-20261024-013#27
═══ */