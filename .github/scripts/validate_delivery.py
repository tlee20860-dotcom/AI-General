#!/usr/bin/env python3
"""交付驗證腳本（機器可驗的規則）

用途：在 setup-structure.yml 打包前，驗證改動的 .md 檔是否符合 C-04 格式。
模式：
  - report（預設）：列出問題，但 exit 0
  - strict：有問題即 exit 1

環境變數：
  VALIDATE_MODE：report / strict
  CHANGED_FILES：換行分隔的檔案路徑（由 yml 提供）
"""

import os
import re
import sys

MODE = os.environ.get("VALIDATE_MODE", "report").strip().lower()
CHANGED = os.environ.get("CHANGED_FILES", "").strip()


def iter_targets():
    """優先使用 CHANGED_FILES；否則掃描 docs/ 下 md 檔（report 模式）"""
    if CHANGED:
        for line in CHANGED.splitlines():
            path = line.strip()
            if path and path.endswith(".md") and os.path.exists(path):
                yield path
        return
    for root, _dirs, files in os.walk("docs"):
        for name in files:
            if name.endswith(".md"):
                yield os.path.join(root, name)


def check_eof(content):
    """EOF 必須有 F/V/W 三行（允許前面有 /* 或 # 等註解符號）"""
    tail = content[-800:]
    m = re.search(r"F:\s*(\S+)\s*\nV:\s*(\d+)\s*\nW:\s*(\S+)", tail)
    if not m:
        return "EOF 缺 F/V/W 三行"
    _f, v, _w = m.groups()
    if len(v) != 10:
        return f"V 不是 10 位 Unix epoch（{v}）"
    return None


def check_inner_backticks(path, content):
    """md 檔內禁止三反引號（F-004）"""
    if not path.endswith(".md"):
        return None
    if "```" in content:
        return "md 內含三反引號（F-004）"
    return None


def check_head(content):
    """檔案開頭必須是 # 標題（F-001 標頭不得寫入檔內）"""
    for line in content.splitlines()[:5]:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            return None
        return f"檔案開頭不是 # 標題（首行為：{s[:40]}）"
    return "檔案為空或前 5 行皆空白"


def validate(path, content):
    problems = []
    for label, fn in (
        ("EOF", lambda c: check_eof(c)),
        ("內層反引號", lambda c: check_inner_backticks(path, c)),
        ("開頭標題", lambda c: check_head(c)),
    ):
        if label == "內層反引號" and not path.endswith(".md"):
            continue
        err = fn(content)
        if err:
            problems.append(err)
    return problems


def main():
    total = 0
    bad = 0
    for path in iter_targets():
        total += 1
        try:
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except Exception as exc:
            print(f"[ERROR] {path}: 讀取失敗（{exc}）")
            bad += 1
            continue
        for msg in validate(path, content):
            print(f"[ERROR] {path}: {msg}")
            bad += 1

    print(f"[SUMMARY] 檢查 {total} 檔，問題 {bad} 項（模式：{MODE}）")
    if bad and MODE == "strict":
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()