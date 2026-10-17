# PATCH 指令

## 修改目標
`docs/common/C-00-startup.md`

## 替換內容
<<<<<<< OLD
未上傳專案包才依 STATE-INDEX 列專案並問情境。
=======
未上傳專案包才依 STATE-INDEX 列專案並問情境。**若已上傳體系包（A00 + S00）且明確表示要進行體系修正，直接生成體系對話編號，不列專案清單、不列 4 選項，直接進入 STATE_DISCUSS**。
>>>>>>> NEW

<<<<<<< OLD
使用者答「對」後，進入 `STATE_WAIT_PROJECT`，停下來等「繼續」。
=======
使用者答「對」後，進入 `STATE_WAIT_PROJECT`，停下來等「繼續」。

> **若已上傳體系包（A00 + S00）且明確表示要進行體系修正**：不列 4 選項、不列專案清單。AI 直接生成體系對話編號（`ai-system-{YYYYMMDD}-{序號3位}`），回覆「🆔 `{對話編號}` #001／📂 所屬專案：`AI 對話系統（體系層）`／已進入 STATE_DISCUSS，請描述修正需求。」（編號與專案名必須用 Code Block 包裹），並直接進入 `STATE_DISCUSS`。
>>>>>>> NEW