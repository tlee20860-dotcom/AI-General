# WF-HANDOFF (p92 UPGRADE-WO)

**records_pending**: []

## 一、專案狀態摘要
本專案已完成重大架構重構，正式進入「完全數據驅動（Data-Driven）」與 PWA 階段。
- **核心架構**：全站工單顯示（卡片、表格、排序、篩選）已統一由 `src/ui/order-view.js` 渲染，採用全域事件委派，徹底解決按鈕失效問題。
- **動態狀態與視圖**：狀態欄位改為下拉選單，點擊即時更新；管理員可於「系統設定 ➜ 視圖配置」自由勾選各頁面要顯示的欄位。
- **PWA 支援**：已加入 `manifest.json` 與 `sw.js`，支援手機「加入主畫面」與離線快取。
- **自動化部署**：CI/CD 改為手動觸發（`.github/workflows/deploy.yml` 改為 `workflow_dispatch`）。
- **背景維護**：系統啟動時會自動在背景掃描並修復舊格式日期（如 46300 轉 YYYY-MM-DD）。

## 二、重建條件
- 系統入口：`index.html` 載入 `/src/engine/main.js`。
- 預設管理員帳密：`admin` / `123456`。
- 資料庫權限：Firestore 規則需設為 `allow read, write: if true;` 以供測試（上線前需替換為正式規則）。
- PWA 圖示：需放置 `public/icons/icon-192.png` 與 `icon-512.png`。

## 三、未完成事項（技術債）
1. **拆分 `settings.js`**：已達約 600 行，未來擴充大型功能（如自訂選單名稱）前，必須先拆分為子模組。
2. **Firebase Auth**：目前為前端明文比對，需升級安全性。

## 四、下一步
- 測試 PWA 安裝與離線快取功能。
- 將 PWA 圖示放入指定資料夾。
- （選配）開始規劃 `settings.js` 的拆分重構。

/* ═══ EOF ═══
F: AI-General/docs/p92/WF-HANDOFF.md
V: 1792916800
W: UPGRADE-002
═══ */