# P-Data (p93 家庭入帳 V3)

用途：記錄本專案的 Supabase PostgreSQL 資料表結構、RLS 權限與連線機制。

---

## 一、連線機制與架構

本專案不使用 Supabase 官方客戶端直連（避免電信商 DNS 封鎖），而是透過 **Cloudflare Pages Functions 進行反向代理**。

- **前端連線**：`src/config/supabase.js` 將網址設為 `window.location.origin + '/api/supabase'`。
- **後端代理**：`functions/api/supabase/[[path]].js` 負責將請求轉發給真實的 Supabase URL，並過濾 Cloudflare 內部標頭以避免 `HTTP 530` 錯誤。

---

## 二、資料表結構 (Tables)

所有資料表皆已啟用 RLS (Row Level Security)，並允許 `authenticated` 與 `anon` 角色進行 CRUD 操作。

### 1. `members` (家庭成員)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID (目前固定為 `00000000-0000-0000-0000-000000000001`) |
| name | text | 成員名稱 (如：老公、老婆) |
| role | text | 角色/關係 |
| created_at | timestamptz | 建立時間 |

### 2. `expense_categories` (支出分類)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID |
| name | text | 分類名稱 (如：日常飲食、交通) |
| created_at | timestamptz | 建立時間 |

### 3. `fixed_expenses` (固定支出模板)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID |
| name | text | 項目名稱 (如：租金) |
| amount | numeric | 金額 |
| payer_name | text | 對象名稱 |
| category_name | text | 分類名稱 |

### 4. `expenses` (收支流水 - 支出)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID |
| year_month | text | 年月 (格式 `YYYY-MM`) |
| name | text | 項目名稱 |
| amount | numeric | 金額 |
| payer_name | text | 對象名稱 |
| category_name | text | 分類名稱 |
| status | text | 狀態 (`未處理` / `已處理`) |
| created_at | timestamptz | 建立時間 |

### 5. `incomes` (收支流水 - 收入)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID |
| year_month | text | 年月 |
| name | text | 收入名稱 |
| amount | numeric | 金額 |
| member_name | text | 對象名稱 |
| created_at | timestamptz | 建立時間 |

### 6. `monthly_balances` (每月銀行對帳)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID |
| year_month | text | 年月 |
| actual_balance | numeric | 實際月結單結餘 |
| created_at | timestamptz | 建立時間 |
*(註：`family_id` + `year_month` 設有 Unique 約束)*

### 7. `insurance_policies` (保單主檔)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID |
| name | text | 保單名稱 |
| company | text | 保險公司 |
| start_date | date | 開始日期 |
| payment_freq | text | 頻率 (`月繳` / `年繳`) |
| premium_amount | numeric | 原始繳費金額 |
| monthly_average | numeric | 平攤後月均金額 |
| total_years | integer | 供款年期 |
| type | text | 類型 (`normal` / `fund_insurance`) |

### 8. `insurance_payments` (保費繳費狀態)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| policy_id | uuid | 關聯保單 ID |
| year_month | text | 年月 |
| status | text | 狀態 (`未轉` / `已轉`) |

### 9. `funds` (基金主檔)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| family_id | uuid | 家庭 ID |
| policy_id | uuid | 關聯保單 ID (若為獨立基金則為 null) |
| name | text | 基金名稱 |
| allocation_pct | numeric | 分配比例 (如 50 代表 50%) |
| manual_cost | numeric | 手動輸入成本 (獨立基金用) |
| withdrawn_amount | numeric | 已提款/轉出金額 |

### 10. `fund_snapshots` (基金每月快照)
| 欄位 | 型態 | 說明 |
|---|---|---|
| id | uuid | 主鍵 |
| fund_id | uuid | 關聯基金 ID |
| year_month | text | 年月 |
| units | numeric | 單位數 |
| nav | numeric | 基金價格 (USD) |
| exchange_rate | numeric | 匯率 |
| total_value_hkd | numeric | 總值 (HKD) |

---

## 三、認證機制

- 使用 **Supabase Auth** (Email + Password)。
- 前端採用「虛擬 Email」機制：使用者輸入 `admin`，前端自動補齊為 `admin@fs-app.com` 進行登入。

/* ═══ EOF ═══
F: AI-General/docs/p93/P-Data.md
V: 1793812200
W: ai-wa-fs-001
═══ */