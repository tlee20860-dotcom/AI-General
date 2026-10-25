## 📄 AI-General/docs/p90/90-P-Map.md

# 90-P-Map（專案地圖與架構）

用途：記錄本專案的目錄結構、V2 依賴契約與舊版架構對照。
說明：通用 ESM 目錄規範與 Page Schema 已抽離至 `W-03` 與 `W-05`，此處僅保留本專案特有實作。

---

## 零、體系規則（W 包）對照表

為確保 AI 處理本專案時能同時遵守體系規範，此表建立 W 包與 P 包的映射關係：

| 體系規則（W 包） | 本專案對應（P 包 / 實作） | 說明 |
|---|---|---|
| `W-01` 資料庫原則 | `90-P-Data.md` | 本專案的 Firebase RTDB 節點結構與 API 契約。 |
| `W-02` 後端規則 | `functions/api/` | CF Pages Functions 的具體實作。 |
| `W-03` 架構與依賴 | `90-P-Map.md`（本檔 §五） | 本專案的目錄結構與具體 import 限制。 |
| `W-05` UI 規範 | `ui/` 與 `pages/` | 本專案頁面的 Schema 與佈局。 |
| `W-07` 錯誤防呆 | `90-P-Errors.md` | 本專案曾踩過的專屬坑（如 Firebase 白屏）。 |

---

## 一、專案目錄結構（V2 現行架構）

> 註：§一 與 §二 保留 V1 舊版結構作為歷史參考。V2 的現行結構請見 §五。

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

---

## 二、HTML 頁面與 Block 對應表（V1 歷史資料）

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

---

## 三、共用模組清單（V1 歷史資料）

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

## 四、關聯檔案

| 主題 | 檔案 |
|---|---|
| 通用 ESM 架構 | `W-03-esmodule.md` |
| 通用 UI Schema | `W-05-schema.md` |
| 資料結構與 API | `90-P-Data.md` |
| 專案業務與防呆 | `90-P-Rules.md` |
| 歷史踩坑 | `90-P-Errors.md` |
| 專案進度 | `WF-PROGRESS.md` |

---

## 五、V2 架構與依賴契約（現行）

本節為本專案在 V2 重構後的實際目錄與依賴對照，AI 必須嚴格遵守 `W-03` 的架構鐵律。

### 5.1 本專案目錄結構（V2）

| 目錄 | 職責 |
|---|---|
| `config/` | `constants.js`、`state.js`、`firebase.js`、`entity-registry.js`、`columns.js`、`status.js`、`app-config.js` |
| `db/` | `read.js`、`write.js`、`index.js` |
| `domain/` | `insurance.js`、`settlement.js`、`fund.js`、`bank.js`、`api-client.js`、`auth.js` |
| `engine/` | `main.js`、`router.js` |
| `pages/` | `dashboard.js`、`input-center.js`、`insurance.js`、`portfolio.js`、`bank.js`、`settlements.js`、`annual-report.js`、`member-report.js`、`settings.js` |
| `ui/` | `layout.js`、`table.js`、`form.js`、`modal.js`、`toast.js`、`controls.js`、`format.js`、`dropdown-plus.js` |
| `lib/` | `expense-modal.js`、`income-modal.js`（業務型 UI 封裝） |

### 5.2 本專案依賴對照

基於 `W-03` 契約，本專案各檔案的允許依賴如下：

| 檔案 | 允許 import | 禁止 import | 說明 |
|---|---|---|---|
| `ui/table.js` | `ui/format.js`、`config/columns.js` | `db/`、`domain/`、`lib/`、`pages/` | 通用表格引擎不可沾染業務邏輯。 |
| `ui/form.js` | `ui/format.js`、`ui/dropdown-plus.js` | `db/`、`domain/`、`pages/` | 表單引擎僅負責渲染與事件綁定。 |
| `domain/insurance.js` | `config/status.js` | `ui/`、`pages/` | 純函式計算，不碰 DOM。 |
| `pages/input-center.js` | `config/`、`db/`、`ui/`、`lib/` | 其他 `pages/` | 頁面只能依賴底層，不可互相依賴。 |
| `lib/expense-modal.js` | `ui/`、`db/`、`config/` | 其他 `pages/` | 業務級 UI 封裝，允許組裝 `ui/` 與 `db/`。 |

### 5.3 AI 自檢要求

依 `W-03 §0.3`，AI 在交付本專案的任何程式碼前，**MUST** 對照 `5.2` 的表格檢查 `import` 區塊。若發現 `ui/` 引入 `db/` 或 `domain/`，必須立即重構。

---

/* ═══ EOF ═══
F: AI-General/docs/p90/90-P-Map.md
V: 1792901610
W: webapp-20261025-001#17
═══ */