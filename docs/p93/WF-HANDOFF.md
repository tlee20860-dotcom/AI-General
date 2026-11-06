# WF-HANDOFF（專案交接快照）

上限：80 行（嚴格限制）
用途：提供下一輪對話 AI 的專案現況快照

---

## 一、當前會話摘要

| 欄位 | 值 |
|---|---|
| 對話編號 | ai-wa-fs-001 |
| 本次範圍 | 從零建立 93 專案（Vue 3 + Element Plus + Supabase），完成所有核心財務功能與資料庫建置 |
| 狀態 | 核心功能已全數上線，等待實機驗收與正式資料錄入 |

---

## 二、議題進度與重大變更

1. **全新架構（取代 90 專案）**：
   - 前端：Vue 3 + Vite + Element Plus + Pinia。
   - 後端：Supabase (PostgreSQL)，捨棄 Firebase RTDB。
   - 部署：Cloudflare Pages。
2. **突破網路封鎖（代理轉發）**：
   - 建立 `functions/api/supabase/[[path]].js`，將對 Supabase 的請求透過 Cloudflare 代理轉發，繞過電信商 DNS 封鎖。
   - 前端 `supabaseUrl` 設為 `window.location.origin + '/api/supabase'`。
3. **虛擬 Email 登入機制**：
   - 帳號輸入 `admin`，系統自動補齊 `@fs-app.com` 作為 Supabase Auth 驗證。
4. **七大核心頁面實作完成**：
   - 工作台（總資產、對帳、分類分析）。
   - 收支流水（表格/看板、固定支出匯入、自訂分類）。
   - 待轉帳表（按對象分組結算）。
   - 保險供款（年繳平攤、自動推算進度、一鍵已轉）。
   - 基金投資（關聯保單自動算成本、歷史快照、提款記錄）。
   - 年度報表（保險與收支統計、CSV 匯出）。
   - 系統設定（成員、分類、固定支出、資料重置）。

---

## 三、重建條件（下一 AI 優先確認）

| # | 優先確認 |
|---|---|
| 1 | 確認 `.github/workflows` 中是否有正確的部署腳本，或依賴 Cloudflare Pages 自動化。 |
| 2 | 確認 Supabase 的 `[[path]].js` 代理是否正常轉發（可查看 Network 狀態碼）。 |
| 3 | 確認 PWA 設定 (`vite.config.js`) 與 `main.js` 中的 `registerSW` 是否正常運作。 |

---

## 四、未完成事項（待執行）

| 項目 | 狀態 |
|---|---|
| 實機測試 PWA 加到主畫面 | 待執行 |
| 將 90 專案正式廢棄或封存 | 待處理 |
| 將 Vue + Supabase 架構經驗寫入 W 包 (W-08) | 待處理 |

---

## 五、下一步建議

| 順序 | 動作 |
|---|---|
| 1 | 使用「系統設定 -> 資料管理」清空所有測試資料，開始正式記帳。 |
| 2 | 檢視「年度報表」與「基金投資」的計算結果是否符合 Excel 預期。 |
| 3 | 將本次架構寫入體系 W 包（`W-08-vue-supabase.md`），完成知識沉澱。 |

/* ═══ EOF ═══
F: AI-General/docs/p93/WF-HANDOFF.md
V: 1793811700
W: ai-wa-fs-001
═══ */