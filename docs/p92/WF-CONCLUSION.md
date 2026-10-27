# WF-CONCLUSION (p92 UPGRADE-WO)

**最後更新時間**: 2026-10-27

## 一、專案架構決策紀錄

| 編號 | 決策主題 | 決策內容 | 原因與備註 |
|---|---|---|---|
| D-92-001 | 前端架構模式 | 採用 Mode B（Vite + Vanilla JS + Tailwind CSS）。 | 專案包含複雜的 Excel 解析、PDF 匯出與多視圖切換，需要現代化構建工具與模組化管理。 |
| D-92-002 | Firebase 金鑰存放 | 建立 `src/config/firebase-keys.js` 直接寫入配置，豁免 `.env` 機制。 | 因使用者初期無電腦環境可建立隱藏檔，且前端 `apiKey` 本身為公開性質。未來有環境時建議改回環境變數。 |
| D-92-003 | Kanban 流轉互動 | 點擊卡片展開「下拉清單」，選擇目標工序進行流轉。 | 取代全螢幕 Modal 彈窗，減少操作層級，提升流水線控制台的直覺性與流暢度。 |
| D-92-004 | Excel 防覆寫機制 | 在 `settings.js` 的匯入流程中，先透過 `getDocument` 檢查 ID，存在則跳過。 | 嚴格遵守「防覆寫」需求，避免重複匯入導致現場工單狀態被重設。 |
| D-92-005 | 權限與角色隔離 | 登入時比對自訂的 `users` 集合（預設 admin/123456），不依賴 Firebase Auth。 | 符合初期輕量化需求。管理員（admin）可流轉工單與修改設定；一般使用者（user）僅能檢視。 |
| D-92-006 | UI/UX 視覺規範 | 全面套用 Modern Soft SaaS Style（`glass-card`、`btn-primary`、iOS 分段控制器）。 | 提供現代化、具備物理回饋感（按壓縮放、柔和陰影）的操作介面。 |

## 二、已知技術債與限制
- Firestore 目前為測試模式（`allow read, write: if true;`），需在上線前替換為正式安全規則。
- 目前尚未實作真正的 Firebase Auth，帳密驗證為前端明文比對，安全性較低。

/* ═══ EOF ═══
F: AI-General/docs/p92/WF-CONCLUSION.md
V: 1792904003
W: UPGRADE-001
═══ */