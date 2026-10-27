# WF-HANDOFF (p92 UPGRADE-WO)

**records_pending**: []

## 一、專案狀態摘要
本專案已完成第一階段核心初始化（W-06 零到一啟動 SOP）。
- 技術棧：Vite + Vanilla JS + Tailwind CSS + Firebase Firestore + SheetJS + jsPDF。
- 架構：嚴格遵守 `W-03` 依賴方向（config -> db -> domain -> ui -> pages）。
- 目前進度：已交付 29 個核心檔案，包含 Kanban、Table、Overview、Salesperson、Settings 等視圖，以及 Excel 匯入解析與 PDF/Excel 匯出功能。

## 二、重建條件
- 系統入口：`index.html` 載入 `/src/engine/main.js`。
- 預設管理員帳密：`admin` / `123456`（若 `settings/main` 為空，登入頁會自動 Fallback）。
- Firebase 配置：直接寫死於 `src/config/firebase-keys.js`（因目前無本地環境變數）。

## 三、未完成事項
1. `settings.js` 的「匯入 Excel」功能尚未在真實 Firebase 環境中進行端到端測試。
2. Cloudflare Pages 尚未設定環境變數與測試自動化部署。
3. Firestore 安全性規則目前為測試模式（`allow read, write: if true;`），30 天後需更新。

## 四、下一步
- 進入測試階段：請將 `npm install` 與 `npm run dev` 跑通，並確認 Firebase 連線正常。
- 測試登入 -> 匯入 Excel -> Kanban 流轉 -> 匯出報表。

/* ═══ EOF ═══
F: AI-General/docs/p92/WF-HANDOFF.md
V: 1792904001
W: UPGRADE-001
═══ */