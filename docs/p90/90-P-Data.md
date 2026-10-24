# 90-P-Data（資料結構與 API 契約）

用途：記錄本專案的 Firebase RTDB 節點與 API 契約。
說明：通用 CF Functions 規範與錯誤碼請見 `W-02`，通用 RTDB 原則請見 `W-01`。此處僅列專案專屬實作。

---

## 一、專案 API 契約

### 1.1 後端端點分派
所有 URL 路徑保持不變；實作改為 `functions/api/[[path]].js` Catch-all 分派。

*   **GET 端點**：`/api/family-settings`、`/api/summary`、`/api/annual-summary` 等。
*   **POST 端點**：`/api/lookup-family`、`/api/entity-create` 等。

### 1.2 核心端點：`POST /api/entity-create`

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
| error | HTTP | 觸發 |
|---|---|---|
| CODE_DUPLICATE | 409 | 編號已存在 |
| NAME_DUPLICATE | 409 | 名稱重複 |

**後端檢查順序**：驗證登入 → 驗證 body → 驗證必填 → 查重複 code → 查重複 name → 寫入 Firebase。

---

## 二、Firebase RTDB 資料結構

### 2.1 platform 節點

| 路徑 | 欄位 / 內容 |
|---|---|
| `families/{familyId}/` | name / ownerEmail / createdAt |
| `families/{familyId}/memberAccounts/{uid}/` | email / account / displayName / role / canInput / memberId / createdAt |
| `platform/uid_index/{uid}` | familyId |
| `platform/email_index/{account}` | { uid, familyId } |
| `platform/defaults/` | members / banks / payment_methods / categories 等預設基礎 |

### 2.2 families 節點

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

---

## 三、狀態代碼與跨節點關聯

**新代碼**：pending (false) / done (true) / skipped (true)。
**舊名稱 → 新代碼**：未處理/未還款/未付款 → pending；已處理/已還款/已付款 → done。

**跨節點關聯**：
*   expenses.*.bankId → bank_accounts/{bankId}
*   expenses.*.txnId → bank_accounts/{bankId}/transactions/{txnId}
*   insurance_policies.advanceId → member_advances/{advanceHolderId}/{advanceId}
*   insurance_policies.fundsAllocation[].fundId → funds/{fundId}
*   funds.policyId → insurance_policies/{policyId}

### 舊資料相容與基金累積流程

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
| 專案架構 | `90-P-Map.md` |
| 專案業務與防呆 | `90-P-Rules.md` |
| 歷史踩坑 | `90-P-Errors.md` |

/* ═══ EOF ═══
F: AI-General/docs/p90/90-P-Data.md
V: 1792900061
W: ai-system-20261024-012#86
═══ */