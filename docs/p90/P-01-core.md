# P-01 專案核心：架構、頁面地圖與 SOP

用途：整合專案技術架構、HTML 對應表與專案專屬 SOP，供 AI 修改 129 檔架構時參考。

---

## 一、專案身份與架構

| 項目 | 內容 |
|---|---|
| 專案 | 家庭財務與固定供款管理 Web App（舊版 129 檔架構） |
| 領域 | W（Web App） |
| GitHub（程式碼） | `tlee20860-dotcom/old-AI-WA-FAMILY` |
| 部署 | Cloudflare Pages |
| 資料庫 | Firebase RTDB (asia-southeast1) |
| 前端 | 純 HTML + CSS + ES Module JS |
| 後端 | Cloudflare Pages Functions |
| 視覺 | 亮色家庭暖陽 |

### 1.1 目錄結構

> **通用目錄規範已抽離至 `W-03-esmodule.md` §八。以下僅列本專案特有之實作與檔數。**

| 目錄 | 檔數 | 內容（專案特有補充） |
|---|---|---|
| js/config | 8+1 | 4 Registry / page-metadata-registry /（待）code-registry |
| js/core | 8 | state / api / db / auth / auth-guard / utils / pwa / debug |
| js/lib | 14 | dom / async / lifecycle / registry / merge / insurance / bank / format / expense-modal / income-modal / filter-sort / page-controls / code-registry / id-resolver |
| js/engines | 3 | page / data / render |
| js/blocks | 5 | stats / list / filter / detail / form |
| js/ui | 7 | toast / modal / form-builder / tab-panel / view-toggle / collapsible / dropdown-plus |
| js/layout | 3 | navbar / sidebar / app-shell |
| js/entity | 5 | entity-modal / entity-helpers / entity-definitions / entity-resolvers / entity-funds-allocation |
| js/admin | 2 | admin / platform-defaults |
| js/shared | 13 | data-table / data-card / ... / yearrange-card |
| js/pages | 10 | 純 Schema |
| functions/api | 11 | _config / _helpers / _admin / _bank / _family / _insurance / _personal / _platform / _summary / _entity / [[path]] |
| CSS | 6 | theme / layout / components / utilities / pages/annual-report / pages/insurance |
| HTML | 13 | 各頁 + login / register + code-list |
| icons | 1+ | icon.svg / icon.png |
| 根目錄 | 3 | sw.js / manifest.json / docs/ |

### 1.2 編號系統與 API 統一

| 模組 | 職責 |
|---|---|
| `js/lib/code-registry.js` | 生成編號（查最大 + 1）、子類短碼自動決定 |
| `js/lib/id-resolver.js` | 從編號查實體、從編號展開關聯 |
| `code-list.html` + `js/pages/code-list.js` | 編號對照清單頁（取代 database.html） |
| `POST /api/entity-create` | 統一新增端點（含 action 參數） |

---

## 二、頁面與檔案對照表（Pagemap）

### 2.1 總覽

| 頁面 | HTML | Schema | 主要 Blocks |
|---|---|---|---|
| 登入 | login.html | — | — |
| 註冊 | register.html | — | — |
| 平台管理 | admin.html | — | （admin.js） |
| 總覽儀表板 | index.html | dashboard.js | stats |
| 綜合輸入中心 | input-center.html | input-center.js | — |
| 編號對照清單 | code-list.html | code-list.js | — |
| 保險清單表 | insurance.html | insurance.js | — |
| 基金投資表 | portfolio.html | portfolio.js | stats |
| 結算清單 | settlements.html | settlements.js | — |
| 銀行交易 | finance-overview.html | finance-overview.js | — |
| 年度報表 | annual-report.html | annual-report.js | stats |
| 成員報表 | member-report.html | member-report.js | stats |
| 系統設定 | settings.html | settings.js | — |

### 2.2 共用模組（所有主頁）

| 檔案 | 職責 |
|---|---|
| js/layout/app-shell.js | App Shell 初始化 |
| js/layout/sidebar.js | 側邊欄（依角色過濾） |
| js/layout/navbar.js | 頂部導覽 |
| js/core/auth-guard.js | 登入驗證 |
| js/core/state.js | 全域狀態 |
| js/core/api.js | API 呼叫 |
| js/core/db.js | Firebase 讀寫 |
| js/core/pwa.js | PWA |
| js/core/debug.js | vConsole |
| js/config/app-config.js | 平台 / 家庭設定 |
| js/config/firebase-config.js | Firebase |
| js/config/page-metadata-registry.js | 頁面 metadata 預設 |
| js/lib/registry.js | Registry 統一初始化 |

---

## 三、專案專屬 SOP

> **通用流程（如新增頁面、部署驗證、緊急回滾）請見 `W-06-sop.md`。此處僅列本專案專屬動作。**

### 3.1 修 Bug 專屬步驟
1. 讀 `P-10-incident.md`
2. 讀 `P-99-errors-map.md`
3. 跑 5 問自檢（體系 R-00）
4. 複現問題、診斷根本原因
5. 提供「診斷 + 方案」待確認
6. 交付後更新 WF-STATE-INDEX + WF-PROGRESS

### 3.2 新增頁面專屬步驟（結合 W-06 §一）
1. 遵循 W-06 通用步驟（寫 `js/pages`、`html`、更新 `sw.js`）
2. 更新 `js/config/constants.js` 的 `SIDEBAR_GROUPS` / `ROUTES`
3. 更新 `P-06-pagemap` 頁面區塊規格（本檔 §二）
4. 更新 `WF-STATE-INDEX` + `WF-PROGRESS`

### 3.3 改 Functions API 專屬步驟（結合 W-02）
1. 讀 `P-08-api.md` + `W-02`
2. 決定哪個 `_xxx.js`
3. 改 handler
4. 若加新端點 → 改 `[[path]].js` 分派
5. 更新 `P-08` + `WF-STATE-INDEX`

**禁止**：新增獨立 `xxx.js` / 用 shim re-export。

### 3.4 變更影響矩陣

| 改動 | 同步更新 |
|---|---|
| 新增頁面 | WF-STATE-INDEX / WF-PROGRESS / P-06 / sw.js / constants.js |
| 改 API | P-08 / WF-STATE-INDEX |
| 改資料結構 | P-09-data |
| 修 Bug | P-10 / WF-PROGRESS / WF-STATE-INDEX |
| 改 Web App 通用 | W-* |

---

## 四、關聯檔案

| 主題 | 檔案 |
|---|---|
| 通用架構 | `W-03-esmodule.md` |
| 通用 SOP | `W-06-sop.md` |
| 通用 API 規則 | `W-02-functions.md` |
| 資料結構 | `P-02-spec.md` |
| 歷史與防呆 | `P-03-history.md` |
| 進度 | `WF-PROGRESS.md` |

/* ═══ EOF ═══
F: AI-General/docs/p90/P-01-core.md
V: 1792900057
W: ai-system-20261024-012#76
═══ */