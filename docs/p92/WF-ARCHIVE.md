# WF-ARCHIVE (p92 UPGRADE-WO)

**最後更新時間**: 2026-11-09
**用途**: 累積型歸檔檔，存放已封存、已過期或已由新檔取代的歷史資訊。主紀錄檔（`WF-HANDOFF`、`WF-PROGRESS`、`WF-CONCLUSION`）不再承載的舊資料，統一搬移至本檔。

---

## 一、記錄原則

| # | 原則 |
|---|---|
| 1 | 本檔為累積型，只增不刪；舊區塊不修改。 |
| 2 | 歸檔觸發時機：主紀錄檔中的舊資料已無即時參考價值、且為騰出篇幅需移出時。 |
| 3 | 每次歸檔在檔案末尾新增一個「歸檔批次」區塊，標明歸檔日期與來源檔。 |
| 4 | 歸檔內容 MUST 保留原始語意，禁止摘要壓縮；若需摘要，另立「摘要」小節，原文仍保留。 |
| 5 | 禁止使用省略詞彙；若原資料含省略，歸檔時如實保留。 |

---

## 二、歸檔批次清單

| 批次 | 歸檔日期 | 來源 | 內容摘要 |
|---|---|---|---|
| B-001 | 2026-11-09 | `P-Architecture.md`、`P-Data.md`、`P-Dev-SOP.md` | SV14 遷移時，舊 `P-*` 技術檔已由 `WF-ARCH.md`、`WF-DATA.md`、`WF-SOP.md` 取代；原檔內容已完整移轉至新檔，本批次僅記錄「舊檔已封存」之事實與路徑。 |

---

## 三、歸檔批次 B-001（2026-11-09）

### 3.1 歸檔原因

體系於 2026-11-09 升級至 SV14，專案紀錄架構全面改為七寶對稱（`WF-HANDOFF`、`WF-PROGRESS`、`WF-CONCLUSION`、`WF-EVOLUTION`、`WF-REJECTED`、`WF-DEBT`、`WF-ARCHIVE`），並廢除 `P-*` 命名（詞 101、A-00 §4.4）。原有技術檔因此更名：

| 舊路徑 | 新路徑 | 處置 |
|---|---|---|
| `AI-General/docs/p92/P-Architecture.md` | `AI-General/docs/p92/WF-ARCH.md` | 內容完整移轉，舊檔由控制台刪除 |
| `AI-General/docs/p92/P-Data.md` | `AI-General/docs/p92/WF-DATA.md` | 內容完整移轉，舊檔由控制台刪除 |
| `AI-General/docs/p92/P-Dev-SOP.md` | `AI-General/docs/p92/WF-SOP.md` | 內容完整移轉，舊檔由控制台刪除 |

### 3.2 舊檔內容處置說明

| 舊檔 | 內容是否保留 | 說明 |
|---|---|---|
| `P-Architecture.md` | 是（移至 `WF-ARCH.md`） | 原文所有章節（核心架構原則、關鍵機制說明、未來重構待辦）已逐字保留於 `WF-ARCH.md`；本次遷移僅更名與補充 SV14 對齊說明，未刪減原有技術內容。 |
| `P-Data.md` | 是（移至 `WF-DATA.md`） | 原文所有章節（資料集說明、動態 Schema 機制）已逐字保留於 `WF-DATA.md`。 |
| `P-Dev-SOP.md` | 是（移至 `WF-SOP.md`） | 原文所有章節（新增頁面步驟、資料過濾邏輯、新增動態欄位）已逐字保留於 `WF-SOP.md`。 |

### 3.3 舊檔 EOF 記錄（供追溯）

以下為舊檔最後一組 EOF 標記，供必要時核對版本：

| 舊檔 | F 欄位 | V 欄位 | W 欄位 |
|---|---|---|---|
| `P-Architecture.md` | `AI-General/docs/p92/P-Architecture.md` | `1793074000` | `UPGRADE-007` |
| `P-Data.md` | `AI-General/docs/p92/P-Data.md` | `1792915500` | `UPGRADE-002` |
| `P-Dev-SOP.md` | `AI-General/docs/p92/P-Dev-SOP.md` | `1792915600` | `UPGRADE-002` |

### 3.4 後續注意事項

| # | 事項 | 說明 |
|---|---|---|
| 1 | 舊檔實際刪除需由控制台執行 | 本檔僅記錄歸檔事實；舊路徑的實體刪除由 Ken 於控制台操作，`setup-structure.yml` 掃描規則需同步改為僅讀 `WF-*`（見 TD-92-010）。 |
| 2 | 若日後需查閱舊檔原文 | 舊檔內容已完整保留於對應新檔；無需保留 `P-*` 副本。若對新檔內容有疑義，以本次歸檔記錄的 EOF 版本號為基準追溯。 |
| 3 | 本批次不歸檔主紀錄檔內容 | `WF-HANDOFF`、`WF-PROGRESS`、`WF-CONCLUSION` 目前篇幅正常，無需搬移；未來若超過合理行數，再行歸檔。 |

---

## 四、後續歸檔提示

| 情境 | 是否歸檔 |
|---|---|
| `WF-HANDOFF.md` 超過 80 行 | 是（將已完成的舊任務摘要搬入本檔） |
| `WF-PROGRESS.md` 已完成階段過多 | 是（將已完成的舊階段搬入本檔） |
| `WF-CONCLUSION.md` 決策編號過多（如超過 100 筆） | 是（將早期決策搬入本檔，保留編號索引） |
| `WF-EVOLUTION.md` 進化史過長 | 是（將早期進化記錄搬入本檔） |
| 單純的程式碼變更 | 否 |
| 技術檔更名 | 是（記錄舊路徑與 EOF，如本批次 B-001） |

/* ═══ EOF ═══
F: AI-General/docs/p92/WF-ARCHIVE.md
V: 1794184000
W: UPGRADE-008
═══ */