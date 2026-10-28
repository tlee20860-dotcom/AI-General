# SYSTEM-ARCHIVE（歸檔台帳）

用途：集中存放累積型檔案的舊資料，減輕正文負擔；正文僅留節尾一行指標。
模式：APPEND_ONLY（只追加，不改舊條目）。
上限：無（追加式，長期累積）。

---

## 一、歸檔規則

| 項目 | 內容 |
|---|---|
| 對象 | 會累積變大的檔案：`SYSTEM-REJECTED.md`、`SYSTEM-DEBT.md`、`R-04-learning.md`、`PROGRESS.md`、`SYSTEM-CONCLUSION.md` |
| 門檻 | REJECTED 50 條／DEBT 已解決者／R-04 50 條／PROGRESS 已完成 10 任務／CONCLUSION 已結案議題 |
| 動作 | 舊資料搬至本檔對應節；正文該節末尾留一行：`（本節已歸檔 N 條，見 SYSTEM-ARCHIVE.md §{節名}）` |
| 編號 | 歸檔不改號；正文與本檔編號一致 |
| 歷史 | 本檔即歷史；不得刪除已歸檔條目 |
| 觸發 | 手動（Ken 說「歸檔」）或達門檻 |

---

## 二、歸檔分區

### §一 REJECTED 歸檔

| 原編號 | 原文摘要 | 歸檔日期 | 來源檔 |
|---|---|---|---|
| （待歸檔） | — | — | `SYSTEM-REJECTED.md` |

### §二 DEBT 歸檔（已解決）

| 原編號 | 原文摘要 | 解決對話 | 歸檔日期 | 來源檔 |
|---|---|---|---|---|
| （待歸檔） | — | — | — | `SYSTEM-DEBT.md` |

### §三 R-04 歸檔

| 原編號 | 原文摘要 | 歸檔日期 | 來源檔 |
|---|---|---|---|
| （待歸檔） | — | — | `R-04-learning.md` |

### §四 PROGRESS 歸檔

| 任務編號 | 任務名稱 | 完成日期 | 歸檔日期 | 來源檔 |
|---|---|---|---|---|
| 012 | 舊對話交接留痕（Webapp V2 重寫） | 2026-10-25 | 2026-10-25 | `SYSTEM-HANDOFF`（ai-system-20261024-012） |

### §五 CONCLUSION 歸檔

| 議題編號 | 議題名稱 | 結案日期 | 歸檔日期 | 來源檔 |
|---|---|---|---|---|
| （待歸檔） | — | — | — | `SYSTEM-CONCLUSION.md` |

---

## 三、與 EVOLUTION 的分工

| 檔案 | 記什麼 | 不記什麼 |
|---|---|---|
| `SYSTEM-EVOLUTION.md` | 體系形態的架構級變化、載體搬遷、制度誕生、條文廢除 | 任務進度、台帳明細 |
| `SYSTEM-ARCHIVE.md`（本檔） | 累積型檔的舊資料（REJECTED／DEBT／R-04／PROGRESS／CONCLUSION） | 形態變化、規則條文 |

---

## 四、歸檔格式

每條歸檔記錄須含：

| 欄位 | 說明 |
|---|---|
| 原編號 | 與來源檔一致，不改號 |
| 原文摘要 | 保留核心語意，不逐字複製 |
| 歸檔日期 | `YYYY-MM-DD` |
| 來源檔 | 原檔路徑 |
| 補充 | DEBT 加「解決對話」；PROGRESS 加「完成日期」；CONCLUSION 加「結案日期」 |

F: AI-General/docs/records/SYSTEM-ARCHIVE.md
V: 1792912600
W: ai-system-004
<!-- === FILE END: AI-General/docs/records/SYSTEM-ARCHIVE.md === -->