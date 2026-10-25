# WF-PROGRESS（專案任務進度追蹤）

用途：追蹤 WebApp Family 專案的步驟進度

---

## 一、當前任務

### 任務 B35-1：全專案模組化重構與 UI 統一（V2）
| 欄位 | 值 |
|---|---|
| 任務名稱 | 舊版 119 檔架構廢棄，重寫為 SPA + 模組化架構，並統一 UI 排版 |
| 開始時間 | 2026-10-24 |
| 當前階段 | 核心架構與功能已完成，全站排版已統一，等待全面功能驗收 |
| 完成度 | 9/10 |

---

## 二、步驟清單

| # | 步驟 | 狀態 | 備註 |
|---|---|---|---|
| 1 | 清空舊版程式碼並建立新目錄結構 | 已完成 | 透過 GitHub Actions 腳本清空 |
| 2 | 建立 P0 骨架（index.html, manifest, sw） | 已完成 | 支援 V2 隔離與 PWA |
| 3 | 建立 P1 設定層（constants, firebase, state） | 已完成 | 狀態與設定全面重構 |
| 4 | 建立 P2 資料層（db/read.js, db/write.js） | 已完成 | 拆分舊版巨型 db.js |
| 5 | 建立 P3 業務域（insurance, settlement, fund） | 已完成 | 純函數化，易於測試 |
| 6 | 建立 P4 後端層（functions/api/） | 已完成 | 修正 405 錯誤，改為 functions 目錄 |
| 7 | 建立 P5 UI 層（table, controls, form） | 已完成 | 支援表格/卡片切換 |
| 8 | 建立 P6 頁面層（dashboard, insurance, input-center 等） | 已完成 | 核心頁面邏輯與 Modal 已補齊 |
| 9 | 建立統一排版引擎 `renderPageLayout` | 已完成 | 封裝於 `ui/layout.js` |
| 10 | 套用統一排版至全站頁面 | 已完成 | 包含 dashboard, portfolio, bank, settlements, code-list, member-report, input-center, annual-report 等 |
| 11 | 全面功能驗收與線上測試 | 待處理 | 需測試 Firebase 寫入與扣款連動，留待下一輪對話執行 |

---

## 三、狀態定義

| 標記 | 意義 |
|---|---|
| 已完成 | 任務已結束 |
| 待處理 | 尚未開始或進行中 |
| 討論中 | 正在規劃方案 |
| 已交付待確認 | 等待使用者驗收 |
| 需重新交付 | 內容有誤需重做 |
| 已廢棄 | 不再執行 |

---

/* ═══ EOF ═══
F: AI-General/docs/p90/WF-PROGRESS.md
V: 1792901090
W: ai-system-20261024-012#13
═══ EOF ═══ */