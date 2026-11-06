# WF-Evolution (p93 架構演進歷史)

用途：記錄本專案從 90 版演進至 93 版的重大架構變革與開發踩坑經驗。此檔案為專案獨立歷史，不與體系全域歷史混合。

---

## 一、舊版 90 專案的痛點

在 90 專案（AI-WEB-APP-Family）時期，我們採用的是：
- **前端**：Vanilla JS + 手寫 DOM 字串 + 自製事件總線。
- **後端**：Firebase RTDB + Cloudflare Functions。
- **問題**：
  1. **UI 體驗不佳**：手寫 HTML 導致排版僵化，缺乏現代化的組件庫支援。
  2. **設定僵化**：許多分類與選項寫死在程式碼中，使用者無法自行新增。
  3. **操作不流暢**：每個頁面各自渲染，事件容易漏綁，Modal 在手機端常破版。

---

## 二、架構選型：為何轉向 Vue 3 + Supabase？

為了解決上述痛點，93 專案進行了徹底的重寫（Rewrite）：
- **前端框架**：選擇 **Vue 3 (Composition API) + Element Plus**。宣告式渲染讓資料與畫面自動同步，Element Plus 提供了開箱即用、極具直覺性的 UI 組件（如表格、對話框、日期選擇器）。
- **後端資料庫**：從 Firebase NoSQL 轉向 **Supabase (PostgreSQL)**。關係型資料庫讓我們能輕鬆處理「保單連動基金」、「年度收支彙總」等複雜的關聯式計算。

---

## 三、開發血淚史與技術防呆（踩坑紀錄）

在 93 專案的建置過程中，遇到了幾個致命問題，以下為解決方案：

### 1. 電信商封鎖 Supabase DNS
- **現象**：網頁一直跳出 `Failed to fetch` 或 `DNS_PROBE_FINISHED_NXDOMAIN`。
- **原因**：特定電信商或網路環境封鎖了 `*.supabase.co` 的子網域。
- **解法**：建立 Cloudflare Worker 代理 (`functions/api/supabase/[[path]].js`)，將所有請求先導向自己的網域，再由 Cloudflare 伺服器轉發給 Supabase。

### 2. Cloudflare 代理轉發崩潰 (HTTP 530)
- **現象**：透過 Worker 轉發 POST 請求時，系統直接噴出 `HTTP 530`。
- **原因**：Worker 直接使用了 `new Request(..., request)` 轉發，導致 Cloudflare 內部的 Header（如 `content-length`、`cf-connecting-ip`）發生衝突。
- **解法**：嚴格白名單過濾 Header，並使用 `request.arrayBuffer()` 或 `request.text()` 讀取 Body，回傳前移除 `content-encoding`。

### 3. Supabase Auth 虛擬信箱限制
- **現象**：使用 `admin@family.local` 建立帳號，登入時報錯 `Email address is invalid`。
- **原因**：Supabase 底層拒絕 `.local` 結尾的虛擬信箱格式。
- **解法**：前端登入時，自動將帳號補齊為合法的假網域 `@fs-app.com`。

### 4. PWA 快取導致的幽靈 Bug
- **現象**：程式碼明明改了，GitHub 也 Commit 了，Cloudflare 也顯示部署成功，但手機打開永遠是舊畫面。
- **原因**：`vite-plugin-pwa` 註冊的 Service Worker 死死咬住了舊的快取。
- **解法**：開發階段先在 `vite.config.js` 拔除 PWA 外掛，並在 `main.js` 寫入 `unregister` 清除快取。功能穩定後才重新啟用。

### 5. 手機端 Element Plus 破版
- **現象**：表格在手機上擠壓變形，側邊欄佔據大半螢幕無法滑動。
- **解法**：
  - 表格外層加上 `overflow-x: auto` 與 `min-width`。
  - 側邊欄在手機端改為 `fixed` 定位與 `translateX(-100%)` 隱藏，搭配遮罩層。

---

## 四、V3 專案的重大突破

1. **極高自由度**：使用者可自行新增分類、對象、固定支出模板，系統自動寫入資料庫。
2. **自動連動計算**：只需輸入保單條件，系統自動推算「基金投入成本」與「真實盈虧（含已提款）」。
3. **一目了然的對帳**：輸入銀行實際結餘，系統自動計算差異，秒抓漏記帳目。

/* ═══ EOF ═══
F: AI-General/docs/p93/WF-Evolution.md
V: 1793812400
W: ai-wa-fs-001
═══ */
