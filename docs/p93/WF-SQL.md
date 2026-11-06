# WF-SQL (p93 資料庫建置腳本)

用途：記錄本專案 Supabase (PostgreSQL) 的完整建表、欄位變更與 RLS 權限腳本。
下一手 AI 或開發者可直接複製此區塊至 Supabase SQL Editor 執行，即可無痛還原 100% 的資料庫結構。

---

## 一、完整建置腳本（請依序執行）

```sql
-- 1. 啟用 UUID 擴充
create extension if not exists "uuid-ossp";

-- ==========================================
-- 2. 建立基礎資料表
-- ==========================================

-- 家庭
create table if not exists families (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 家庭成員
create table if not exists members (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    name text not null,
    role text default 'member',
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 支出分類
create table if not exists expense_categories (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    name text not null,
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- ==========================================
-- 3. 銀行與收支表
-- ==========================================

-- 固定支出模板
create table if not exists fixed_expenses (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    name text not null,
    amount numeric not null,
    payer_name text,
    category_name text,
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 支出流水
create table if not exists expenses (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    year_month text not null, -- 例如 '2026-11'
    name text not null,
    amount numeric not null,
    payer_name text, -- 對象名稱
    category_name text, -- 分類名稱
    status text default '未處理',
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 收入流水
create table if not exists incomes (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    year_month text not null,
    name text not null,
    amount numeric not null,
    member_name text,
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 每月銀行結餘 (對帳用)
create table if not exists monthly_balances (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    year_month text not null,
    actual_balance numeric default 0,
    created_at timestamp with time zone default timezone('utc'::text, now()),
    unique(family_id, year_month) -- 確保每個月只有一筆
);

-- ==========================================
-- 4. 保險模組
-- ==========================================

-- 保單主檔
create table if not exists insurance_policies (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    name text not null,
    company text,
    start_date date not null,
    payment_freq text not null, -- '月繳' 或 '年繳'
    premium_amount numeric not null, -- 原始繳費金額
    monthly_average numeric not null, -- 平攤後的月均金額
    total_years integer not null, -- 供款年期
    type text default 'normal', -- 'normal' 或 'fund_insurance'
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 保單繳費狀態
create table if not exists insurance_payments (
    id uuid primary key default uuid_generate_v4(),
    policy_id uuid references insurance_policies(id) on delete cascade,
    year_month text not null,
    status text default '未轉',
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- ==========================================
-- 5. 基金模組
-- ==========================================

-- 基金主檔
create table if not exists funds (
    id uuid primary key default uuid_generate_v4(),
    family_id uuid references families(id) on delete cascade,
    policy_id uuid references insurance_policies(id) on delete set null,
    name text not null,
    allocation_pct numeric default 0, -- 分配比例 (如 50)
    manual_cost numeric default 0, -- 手動輸入成本 (獨立基金用)
    withdrawn_amount numeric default 0, -- 已提款/轉出金額
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- 基金快照
create table if not exists fund_snapshots (
    id uuid primary key default uuid_generate_v4(),
    fund_id uuid references funds(id) on delete cascade,
    year_month text not null,
    units numeric not null,
    nav numeric not null, -- 基金價格 (USD)
    exchange_rate numeric default 7.8,
    total_value_hkd numeric not null,
    created_at timestamp with time zone default timezone('utc'::text, now())
);

-- ==========================================
-- 6. 開啟 RLS 與權限設定
-- ==========================================

-- 開啟所有表的 RLS
alter table families enable row level security;
alter table members enable row level security;
alter table expense_categories enable row level security;
alter table fixed_expenses enable row level security;
alter table expenses enable row level security;
alter table incomes enable row level security;
alter table monthly_balances enable row level security;
alter table insurance_policies enable row level security;
alter table insurance_payments enable row level security;
alter table funds enable row level security;
alter table fund_snapshots enable row level security;

-- 賦予權限 (GRANT)
GRANT ALL PRIVILEGES ON TABLE families TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE members TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE expense_categories TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE fixed_expenses TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE expenses TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE incomes TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE monthly_balances TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE insurance_policies TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE insurance_payments TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE funds TO authenticated, anon;
GRANT ALL PRIVILEGES ON TABLE fund_snapshots TO authenticated, anon;

-- 建立通用 Policy (允許已登入者讀寫所有資料)
DROP POLICY IF EXISTS "Allow all for authenticated users" on families;
CREATE POLICY "Allow all for authenticated users" on families FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on members;
CREATE POLICY "Allow all for authenticated users" on members FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on expense_categories;
CREATE POLICY "Allow all for authenticated users" on expense_categories FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on fixed_expenses;
CREATE POLICY "Allow all for authenticated users" on fixed_expenses FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on expenses;
CREATE POLICY "Allow all for authenticated users" on expenses FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on incomes;
CREATE POLICY "Allow all for authenticated users" on incomes FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on monthly_balances;
CREATE POLICY "Allow all for authenticated users" on monthly_balances FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on insurance_policies;
CREATE POLICY "Allow all for authenticated users" on insurance_policies FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on insurance_payments;
CREATE POLICY "Allow all for authenticated users" on insurance_payments FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on funds;
CREATE POLICY "Allow all for authenticated users" on funds FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow all for authenticated users" on fund_snapshots;
CREATE POLICY "Allow all for authenticated users" on fund_snapshots FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- ==========================================
-- 7. 插入初始預設資料
-- ==========================================

insert into families (id, name) values ('00000000-0000-0000-0000-000000000001', '我的家庭')
on conflict do nothing;

insert into members (family_id, name) values ('00000000-0000-0000-0000-000000000001', '老公')
on conflict do nothing;

insert into members (family_id, name) values ('00000000-0000-0000-0000-000000000001', '老婆')
on conflict do nothing;

insert into members (family_id, name) values ('00000000-0000-0000-0000-000000000001', '家庭共用')
on conflict do nothing;
```

<!-- ═══ EOF ═══
F: AI-General/docs/p93/WF-SQL.md
V: 1793968200
W: ai-wa-fs-002
═══ -->