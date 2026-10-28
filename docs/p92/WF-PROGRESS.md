# WF-PROGRESS (p92 UPGRADE-WO)

**最後更新時間**: 2026-10-28

## 一、開發進度總表

| 階段 | 模組 | 狀態 | 備註 |
|---|---|---|---|
| 1. 環境初始化 | Vite + Tailwind 基礎建設 | ✅ 完成 | 包含 package.json, configs |
| 1. 環境初始化 | Firebase 連線設定 | ✅ 完成 | 金鑰直寫於 firebase-keys.js |
| 2. 骨架與設定 | 狀態管理與常數 | ✅ 完成 | state.js, constants.js |
| 2. 骨架與設定 | 路由與守衛 | ✅ 完成 | router.js, main.js |
| 3. 通用引擎 | 資料層讀寫封裝 | ✅ 完成 | read.js, write.js |
| 3. 通用引擎 | UI 元件封裝 | ✅ 完成 | layout, toast, modal |
| 4. POC 跑通 | 登入機制 | ✅ 完成 | login.js (Fallback 預設 admin) |
| 5. 架構重構 | 全面數據驅動與全域事件委派 | ✅ 完成 | 統一由 `order-view.js` 渲染 |
| 5. 業務填充 | 管理總表與視圖切換 | ✅ 完成 | table.js (含匯出與動態欄位) |
| 5. 業務填充 | 總狀態與類別視圖 | ✅ 完成 | overview.js, category.js |
| 5. 業務填充 | 銷售員視圖 | ✅ 完成 | salesperson.js |
| 6. 系統設定 | 動態 Schema 與視圖配置 | ✅ 完成 | settings.js 可動態勾選顯示欄位 |
| 7. 安全管理 | 管理員專屬資料總管 | ✅ 完成 | admin-data.js 可清空資料庫 |
| 7. 安全管理 | 對照表編輯彈窗優化 | ✅ 完成 | 改為單一表單彈窗 |
| 8. PWA 升級 | 支援「加入主畫面」與快取 | ✅ 完成 | manifest.json, sw.js |

## 二、已完成細節
- **動態 Schema**：可自由新增 Excel 欄位，並透過「視圖配置」決定顯示於何處。
- **狀態直接修改**：表格與卡片中的狀態欄位已改為下拉選單，選擇即存檔。
- **資料清洗**：自動過濾垃圾資料，並由 `main.js` 背景任務自動修正歷史日期。
- **匯入保護**：每日重新匯入 Excel 時，不會覆蓋手動修改的生產進度。
- **管理員總管**：Admin 可進入專屬頁面清除 Firebase 中的無效資料。

## 三、待辦清單 (Next Actions)
- [ ] 上傳 PWA 圖示至 `public/icons/`。
- [ ] 測試 PWA 在手機上的安裝與離線體驗。
- [ ] 評估是否將 `settings.js` 拆分為子模組。

/* ═══ EOF ═══
F: AI-General/docs/p92/WF-PROGRESS.md
V: 1792918200
W: UPGRADE-003
═══ */