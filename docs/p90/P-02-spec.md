# P-02 專案規格：資料結構、API 與業務術語

用途：整合專案專屬的 Firebase DB 結構、API 契約與業務術語，供 AI 修改資料流時參考。

---

## 一、業務術語（專案專屬）

> 通用 UI 結構（如 Page、Section、Card 等）請見 `W-05-schema.md` §九。此處僅列本專案專屬業務詞彙。

### 保險類
| 術語 | 說明 |
|---|---|
| 基金保險 | 投資型保險 |
| 普通保險 | 住院 / 人壽 / 意外 |
| 供滿 | 保單供款年期結束 |
| 平攤 | 將年繳保費按 12 個月分攤 |
| 代墊 | 成員先墊付保費 |
| 保單持有人 | policyHolderId |
| 受保人 | memberId |
| 供款期 | periodIndex |

### 收支類
| 術語 | 說明 |
|---|---|
| 家用轉入 | income 節點 |
| 個人收入 | personal_income 節點 |
| 共同支出 | memberId = 'shared' |
| 額外收入 | extra 節點 |

### 結算類
| 術語 | 說明 |
|---|---|
| 待處理 | pending |
| 已處理 | done |
| 不適用 | skipped |
| 結算清單 | 整合個人支出 / 共同支出 / 保險扣款 |

### 基金類
| 術語 | 說明 |
|---|---|
| 保險基金 | type = 'insurance' |
| 獨立基金 | type = 'standalone' |
| 快照 | 每月記錄 |
| 累積供款 | cumulativeCost |
| 盈虧 | 現值 − 累積供款 |

### 銀行類
| 術語 | 說明 |
|---|---|
| 家庭帳號 | type = 'family' |
| 個人帳號 | type = 'personal' |
| 初始餘額 | initialBalance |
| 銀行交易 | in / out / transfer |

### 角色與編號類
| 術語 | 說明 |
|---|---|
| superadmin / owner / member | 系統角色 |
| code | 實體編號（如 POL-001） |
| 大類前綴 | MEM / PAY / POL / FUND / CAT / ITEM / COMP / INC / TXN |
| 子類短碼 | FUND / NORM / FUNIN / SAVE / SCH / TRA / MED / BNK / OTH |

---

## 二、API 契約（專案專屬）

> 通用 CF Functions 規範與錯誤碼請見 `W-02-functions.md`。此處僅列本專案端點。

### 2.1 後端端點
所有 URL 路徑保持不變；實作改為 `functions/api/[[path]].js` Catch-all 分派。

*   **GET 端點**：`/api/family-settings`、`/api/summary`、`/api/annual-summary` 等。
*   **POST 端點**：`/api/lookup-family`、`/api/entity-create` 等。

### 2.2 核心端點：`POST /api/entity-create`

**Request**：
| 欄位 | 類型 | 說明 |
|---|---|---|
| entityType | string | member / bank / category / item / payment / company / policy / fund / bankAccount |
| action | string | create / update / delete |
| code | string | 前端生成的編號（create 用） |
| name | string | 名稱 |
| id | string | 實體 ID（update / delete 用） |
| extra | object | 依類型不同 |

**成功回應**：`{ ok: true, id, code }`

**本專案專屬錯誤碼**：
| error | 觸發 |
|---|---|
| CODE_DUPLICATE | 編號已存在（HTTP 409） |
| NAME_DUPLICATE | 名稱重複（HTTP 409） |

**後端檢查順序**：驗證登入 → 驗證 body → 驗證必填 → 查重複 code → 查重複 name → 寫入 Firebase。

---

## 三、Firebase RTDB 資料結構

### 3.1 platform 節點

| 路徑 | 欄位 / 內容 |
|---|---|
| `families/{familyId}/` | name / ownerEmail / createdAt |
| `families/{familyId}/memberAccounts/{uid}/` | email / account / displayName / role / canInput / memberId / createdAt |
| `platform/uid_index/{uid}` | familyId |
| `platform/email_index/{account}` | { uid, familyId } |
| `platform/defaults/` | members / banks / payment_methods / categories 等預設基礎 |

### 3.2 families 節點

#### 基礎資料
| 節點 | 欄位 |
|---|---|
| members/{id} | name / role / order / code / createdAt |
| banks/{id} | name / order / code / createdAt（舊節點，部分保留） |
| expense_categories/{id} | name / shortCode / order / code / createdAt |
| expense_items/{id} | name / categoryId / code / createdAt |
| payment_methods/{id} | name / order / code / createdAt |
| insurance_companies/{id} | name / code / createdAt |
| statuses/{id} | name / category / isDone / order / createdAt |

#### 銀行系統
| 路徑 | 欄位 |
|---|---|
| bank_accounts/{bankId} | name / type / ownerType / ownerId / isSystemCreated / initialBalance / initialYear / initialMonth / order / code / createdAt |
| bank_accounts/{bankId}/transactions/{txnId} | type / category / amount / date / memberId / refId / note / code / createdAt |

**交易 type**：in / out / transfer
**交易 category**：contribution / expense / insurance / reimbursement / manual

#### 個人財務與收支
| 路徑 | 內容 |
|---|---|
| personal_income/{memberId}/{year}/{month} | 數字 |
| member_advances/{memberId}/{advanceId} | policyId / totalAmount / remainingAmount / startYear / startMonth / paidMonths / note / createdAt |
| income/{year}/{month}/{memberId} | 數字（額外收入 memberId 為 extra） |
| expenses/{year}/{month}/member_expenses/{memberId}/{expenseId} | name / amount / status / date / categoryId / itemId / paymentMethodId / bankId / txnId / isAutoLinked / policyId / repaidDate / code / createdAt |

**特殊 memberId**：shared（家庭共用）
**特殊 expenseId**：linked_{policyId}（保險連動）

#### 保險與基金
| 路徑 | 欄位 |
|---|---|
| insurance_policies/{policyId} | type / memberId / policyHolderId / name / company / paymentType / paymentMode / advanceHolderId / advanceId / firstStartYear / firstStartMonth / totalPolicyYears / totalPolicyPeriods / totalPremium / currentPeriodIndex / monthlyPremium / annualPremium / account / fundsAllocation / periods / isCompleted / code / createdAt |
| insurance_payments/{policyId}/{year}/{month} | status / amount / date / bankId / txnId / paymentMode |
| funds/{fundId} | name / type / policyId / cost / currentValue / units / initialYear / initialMonth / note / code / createdAt |
| funds/{fundId}/snapshots/{year}/{month} | shares / nav / value / contribution / cumulativeCost / createdAt / updatedAt |

**periods 結構**：`{ '{N}': { periodIndex, startYear, startMonth, annualPremium, monthlyAverage } }`
**fundsAllocation 結構**：`[{ fundId, pct, fromYear, fromMonth }, ...]`
**snapshot.value**：shares × nav（自動計算）

#### 家庭設定與廢除節點
| 節點 | 內容 / 狀態 |
|---|---|
| settings/options | { memberRoles, policyTypes, ... } |
| settings/year_range | { startYear, futureYears } |
| settings/ui_constants | { nameMaxLenDesktop, ... } |
| settings/page_metadata/{pageKey} | { title, subtitleStatic } |
| `bank_balances/` | 廢除（保留不讀寫） |
| `fixed_expenses/` | 廢除（保留不讀寫，`_summary.js` 仍讀取舊資料） |

### 3.3 狀態代碼與跨節點關聯

**新代碼**：pending (false) / done (true) / skipped (true)。
**舊名稱 → 新代碼**：未處理/未還款/未付款 → pending；已處理/已還款/已付款 → done。

**跨節點關聯**：
*   expenses.*.bankId → bank_accounts/{bankId}
*   expenses.*.txnId → bank_accounts/{bankId}/transactions/{txnId}
*   insurance_policies.advanceId → member_advances/{advanceHolderId}/{advanceId}
*   insurance_policies.fundsAllocation[].fundId → funds/{fundId}
*   funds.policyId → insurance_policies/{policyId}

### 3.4 舊資料相容與基金累積流程

**相容清單**：
*   狀態字串：讀取時 `status.normalize(raw)`。
*   `banks/` 節點：由 `entity-registry` 一併註冊。
*   `fixed_expenses/`：保留 `summary.js` 讀取。
*   無 `paymentMode`：fallback 為 `direct`。
*   無 `fundsAllocation`：fallback 為 `[]`。

**基金累積邏輯**：
1. 結算清單改為 done → 呼叫 `api.insuranceSync`。
2. 後端計算 `addCost = monthlyPremium × pct / 100`。
3. 更新 `funds/{fundId}/snapshots/{y}/{m}` 的 `cumulativeCost`。
4. 若改回 pending → 呼叫 `api.insuranceUnsync` 自動回退。

---

## 四、關聯檔案

| 主題 | 檔案 |
|---|---|
| 通用 API 規則 | `W-02-functions.md` |
| 通用 Firebase 原則 | `W-01-firebase.md` |
| 通用 UI 結構 | `W-05-schema.md` |
| 專案核心架構 | `P-01-core.md` |
| 歷史與防呆 | `P-03-history.md` |

/* ═══ EOF ═══
F: AI-General/docs/p90/P-02-spec.md
V: 1792900058
W: ai-system-20261024-012#77
═══ */