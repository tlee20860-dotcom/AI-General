#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATCH_FILE = ROOT / ".github" / "workflows" / "PATCH.md"

FILE_RE = re.compile(r"^## FILE:\s*(.+?)\s*$", re.M)
PAIR_RE = re.compile(
    r"<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW",
    re.S,
)

def main() -> None:
    if not PATCH_FILE.exists():
        print(f"[SKIP] 找不到 {PATCH_FILE}，安全結束。")
        sys.exit(0)

    text = PATCH_FILE.read_text(encoding="utf-8")
    file_matches = list(FILE_RE.finditer(text))
    
    # 若為重置後的空白檔，直接安全結束（不報紅叉）
    if not file_matches:
        print("[SKIP] PATCH.md 內沒有 '## FILE:' 區塊（可能已被重置），安全結束。")
        sys.exit(0)

    planned = []
    errors = []

    for idx, match in enumerate(file_matches):
        rel_path = match.group(1).strip()
        start = match.end()
        end = file_matches[idx + 1].start() if idx + 1 < len(file_matches) else len(text)
        block = text[start:end]

        pairs = PAIR_RE.findall(block)
        if not pairs:
            errors.append(f"{rel_path}: 找不到 OLD/NEW 配對")
            continue

        target = (ROOT / rel_path).resolve()
        if not target.is_file():
            errors.append(f"{rel_path}: 目標檔案不存在")
            continue

        content = target.read_text(encoding="utf-8")
        new_content = content

        for old, new in pairs:
            count = new_content.count(old)
            if count == 1:
                new_content = new_content.replace(old, new, 1)
                print(f"[OK] {rel_path}: 替換 1 處")
            elif count == 0:
                if new in new_content:
                    print(f"[SKIP] {rel_path}: OLD 不存在，但 NEW 已存在（已套用）")
                else:
                    errors.append(f"{rel_path}: OLD 出現 0 次，且 NEW 不存在")
            else:
                errors.append(f"{rel_path}: OLD 出現 {count} 次，非唯一")

        if new_content != content:
            planned.append((target, new_content, rel_path))

    if errors:
        for e in errors:
            print(f"[ERROR] {e}")
        sys.exit(1)

    for target, new_content, rel_path in planned:
        target.write_text(new_content, encoding="utf-8")
        print(f"[WRITE] {rel_path}")

    print(f"[DONE] 共寫入 {len(planned)} 個檔案")
    
    # 重置 PATCH.md
    PATCH_FILE.write_text("# 請在此貼上新的替換指令\n", encoding="utf-8")
    print(f"[RESET] PATCH.md 已重置")

if __name__ == "__main__":
    main()