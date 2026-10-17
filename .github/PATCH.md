# PATCH

## FILE: docs/common/C-04-output.md
<<<<<<< OLD
| 6 | **EOF 同步更新** | 交付 Patch 時，必須包含一段針對檔案底部 `V:`（時間戳）與 `W:`（編寫者）的替換區塊，確保版本同步。 |
=======
| 6 | **EOF 同步更新** | 交付 Patch 時，必須包含一段針對檔案底部 `V:`（時間戳）與 `W:`（編寫者）的替換區塊，確保版本同步。 |
| 7 | **表格替換防呆** | 禁止盲猜 `OLD`。若無截圖確認當前內容，必須使用 `REGEX` 或最末行錨點，嚴防疊加錯位。 |
>>>>>>> NEW

## FILE: docs/common/C-05-learning/system.md
<<<<<<< REGEX
/\* ═══ EOF ═══
=======
- **L-026**：表格類 Patch 易因盲目疊加而錯位，AI 應先求證再交付（使用 REGEX 或末端錨點）。

/\* ═══ EOF ═══
>>>>>>> NEW

## FILE: docs/common/C-04-output.md
<<<<<<< REGEX
V: .*\nB: .*\nW: .*
=======
V: 1792259500
B: B34-5
W: ai-system-20261017-005#075
>>>>>>> NEW

## FILE: docs/common/C-05-learning/system.md
<<<<<<< REGEX
V: .*\nB: .*\nW: .*
=======
V: 1792259500
B: B34-5
W: ai-system-20261017-005#075
>>>>>>> NEW