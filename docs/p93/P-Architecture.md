# P-Architecture (p93 家庭入帳 V3)

用途：記錄本專案的 V3 前端架構、目錄結構與核心設計模式，供後續開發與交接參考。

---

## 一、核心架構原則：宣告式與組件化

本專案已徹底廢除 90 專案的「手寫 DOM 字串」與「自製事件總線」，全面轉向 Vue 3 的宣告式渲染。

### 1. 唯一資料源與響應式 (Reactivity)
- 數據獲取後，直接存入 `ref` 或 `reactive`。
- UI 畫面會由 Vue 自動追蹤變化並重新渲染，**禁止**手動執行 `innerHTML` 或 `appendChild`。

### 2. 組件與路由分離
- **`src/views/`**：每個檔案對應一個獨立的頁面路由（如 `CashflowView.vue`、`FundView.vue`）。
- **`src/App.vue`**：負責全局佈局（側邊欄、頂部導航）與路由出口 (`<router-view />`)。
- **`src/router/index.js`**：負責路由守衛與頁面註冊。

### 3. 資料存取層 (Data Access)
- 所有與資料庫的互動皆透過 **`src/config/supabase.js`** 發起。
- 由於電信商可能封鎖 Supabase 網域，本專案採用 **Cloudflare Worker 代理** (`functions/api/supabase/[[path]].js`)。
- 前端 `supabaseUrl` 固定為 `window.location.origin + '/api/supabase'`，確保請求 100% 走代理。

---

## 二、目錄結構 (V3)

| 目錄/檔案 | 職責 |
|---|---|
| `functions/api/supabase/[[path]].js` | 代理轉發器（防 530 崩潰、繞過網路封鎖）。 |
| `src/config/supabase.js` | 初始化 Supabase Client（含代理網址與 Publishable Key）。 |
| `src/router/index.js` | Vue Router 設定與登入守衛（檢查 Session）。 |
| `src/App.vue` | 全局佈局（側邊欄、Header、Logout、響應式遮罩）。 |
| `src/main.js` | 掛載 Element Plus、Router 與 PWA (`registerSW`)。 |
| `src/views/` | 頁面組件（Dashboard, Cashflow, Settlement, Insurance, Fund, AnnualReport, Settings, Login）。 |
| `src/style.css` | 全局樣式與 Element Plus 覆寫。 |

---

## 三、依賴方向鐵律

| 檔案層級 | 允許依賴 | 禁止依賴 | 說明 |
|---|---|---|---|
| `views/*.vue` | `@/config/supabase`, `element-plus` | 其他 `views/*.vue` | 頁面之間不得互相引用，保持獨立。 |
| `App.vue` | `@/config/supabase`, `vue-router` | `views/*.vue` | 只能透過 `<router-view>` 顯示頁面，不得直接 import 頁面。 |
| `functions/*.js` | 無 | 前端 `src/` 內的任何檔案 | 後端代理與前端環境完全隔離。 |

---

## 四、關鍵設計模式與防呆

### 1. 手機端側邊欄抽屜化
- 傳統的 `el-aside` 在手機上會擠壓內容。
- **解法**：在 `App.vue` 中偵測 `window.innerWidth < 768`，將側邊欄改為 `fixed` 定位並使用 `transform: translateX(-100%)` 隱藏，點擊漢堡選單才滑出。

### 2. 表格橫向滑動 (防破版)
- Element Plus 的 `el-table` 在手機上會強制壓縮欄位。
- **解法**：所有 `el-table` 外層必須包一個 `div.table-wrapper { overflow-x: auto; }`，並設定表格 `min-width`。

### 3. 年繳保費自動平攤
- `InsuranceView.vue` 在新增保單時，會判斷繳費頻率。若為年繳，則在寫入資料庫前自動執行 `Math.round(金額 / 12)`，並存入 `monthly_average` 欄位。

### 4. 基金成本自動推算
- `FundView.vue` 不允許手動輸入關聯基金的「投入成本」。
- **演算法**：抓取關聯保單的 `start_date`，計算至當前月份的差距，得出「已供款月數」。再將 `月均金額 × 已供款月數 × 分配比例`，即時算出當前成本。

### 5. 待轉帳分組
- `SettlementView.vue` 利用 `computed` 屬性，將當月所有 `status !== '已處理'` 的支出，按 `payer_name` 進行分組與加總，並提供一鍵批次結算功能。

/* ═══ EOF ═══
F: AI-General/docs/p93/P-Architecture.md
V: 1793812300
W: ai-wa-fs-001
═══ */