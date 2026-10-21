# SYSTEM-CONCLUSION（體系層滾動結論）

用途：體系層滾動式累積結論（議題 + 設計 + 決策）

---

## 一、議題清單

| # | 議題 | 狀態 |
|---|---|---|
| 1~69 | 歷史議題 | ✅ |
| 70 | Version SSOT 與 Patch 工具缺陷 | ✅ |
| 71 | W 包重構與專案紀錄 WF 對齊 | ✅ |
| 72 | 體系微核心化 v1.5（DSL／FSM／STATE_SEAL） | ✅ |

---

## 二、設計結論

*(2.1~2.22 保留原樣)*

### 2.23 體系 v3 重構（003 定案）
*(原 10 點保留)*

### 2.24 W 包與自動化對齊（004 定案）
1. **W 包現代化**：擴充至 W-00~W-07（新增通用 SOP 與錯誤），完全拔除專案綁定字眼。
2. **紀錄分離**：專案紀錄檔對齊 AI-G 命名（WF-*）；決策與錯誤明細降級為 P-04/14/99。
3. **腳本自治**：`setup-structure.yml` 不只打包，還負責生成並回寫專案的 `WF-STATE-INDEX.md`。
4. **防撞機制**：專案 `notify.yml` 忽略 `WF-STATE-INDEX.md`，阻斷無限迴圈。

### 2.25 體系微核心化 v1.5（006 定案）
1. **FSM 結構化**：T99 移出 transitions 改 `fallback_handler`；`evaluation_order: strict_top_down`；四步求值（boot_check → pending → transitions → fallback）。
2. **開場版本比對**：`boot_check` 抓「改過四檔卻未結案」；口頭決策遺失抓不到。
3. **pending 攔截**：`records_pending` 單一真相在 HANDOFF 檔頭；只擋交付，不擋討論。
4. **FastDev 自檢**：主走 GitHub Actions 正則；無 CI 時提取式＋Ken 抽查。
5. **R-011 補強**：物理關鍵字否定清單＋`domain_classification` 宣告。
6. **F-004 例外**：md 檔內含 YAML 時，外層 MUST 用四反引號。
7. **SP 擴為六檔**：新增 `SYSTEM-REJECTED.md`、`SYSTEM-DEBT.md`，皆 APPEND_ONLY。
8. **STATE_SEAL**：取代長篇交接詞，ssot 指向六檔，`rejected_options`／`tech_debts` 帶 RJ／K 編號。

---

## 三、決策記錄

*(D-198~D-343 保留原樣)*

| 編號 | 決策 | 說明 |
|---|---|---|
| D-144 | W 包擴充並中性化 | W-00~W-07；拔除特定專案字眼。 |
| D-145 | 專案紀錄檔改名 WF-* | 對齊 AI-G；P-02/03/12/13 廢除並轉型。 |
| D-146 | 體系代管專案索引生成 | `setup-structure.yml` 增加 Step 7.5 與 9。 |
| D-147 | 腳本防呆 | 加入 `if [ -d "docs/projects" ]` 避免空目錄崩潰。 |
| D-148 | R-00 F-007 語法補齊 | 納入 REGEX 與 REPLACE_ALL。 |
| D-149 | `entity-registry.js` code 留待專案 | 屬業務邏輯，由專案對話處理。 |
| D-150 | FSM 改 `fallback_handler` | T99 留 transitions 無法物理保證最後匹配。 |
| D-151 | 加 `boot_check` 開場版本比對 | 抓「改過四檔卻未結案」；口頭決策抓不到。 |
| D-152 | `records_pending` 單一真相在 HANDOFF | 其他三檔不重複加，避免多處真相。 |
| D-153 | SP 擴為六檔 | 新建 REJECTED／DEBT，皆 APPEND_ONLY。 |
| D-154 | F-004 加四反引號例外 | md 內含 YAML 時外層用 ````。 |
| D-155 | FastDev 自檢主走 CI、次走提取式 | 無 CI 時提取原文＋Ken 抽查。 |
| D-156 | R-05-dsl-map 新增 | 36 條映射：30 DSL、4 散文、2 部分 DSL。 |

**決策明細**：被否決方案見 `SYSTEM-REJECTED.md`（RJ-xxx）；技術債見 `SYSTEM-DEBT.md`（K-xx／C-xx）。

---

## 四、關聯檔案

| 主題 | 檔案 |
|---|---|
| 體系層交接 | SYSTEM-HANDOFF.md |
| 任務進度 | PROGRESS.md |
| 被否決方案台帳 | SYSTEM-REJECTED.md |
| 技術債台帳 | SYSTEM-DEBT.md |
| 檔案清單索引 | STATE-INDEX.md |
| 身份與信仰 | I-00-identity.md（合成物 IP） |
| 啟動引導 | A-00-guide.md（合成物 AP） |
| 核心規則 | R-00-rules.md（合成物 RP） |
| 規則 DSL 映射 | R-05-dsl-map.md（合成物 RP） |
| 使用者畫像 | U-00-profile.md（合成物 UP） |

/* ═══ EOF ═══
F: AI-General/docs/records/SYSTEM-CONCLUSION.md
V: 1792600033
W: ai-system-20261021-006#11
═══ */