import sys
import os
import re

# 強制以當前工作目錄（Repo 根目錄）為基準
patch_file = ".github/workflows/PATCH.md"

if not os.path.exists(patch_file):
    print("PATCH.md not found")
    sys.exit(0)

with open(patch_file, "r", encoding="utf-8") as f:
    text = f.read()

if "## FILE:" not in text:
    print("PATCH.md is empty or reset. Exiting safely.")
    sys.exit(0)

# 完美正則：只抓取 ## FILE: 後面的路徑與區塊內容，完全忽略前面的任何註解
pattern = re.compile(r"## FILE:\s*(.*?)\n(.*?)(?=## FILE:|\Z)", re.S)
matches = pattern.findall(text)

planned = []
errors = []

for rel_path, content_block in matches:
    rel_path = rel_path.strip()
    if not os.path.exists(rel_path):
        errors.append(f"{rel_path}: File not found")
        continue
        
    with open(rel_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    new_content = content
    pairs = re.findall(r"<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW", content_block, re.S)
    if not pairs:
        errors.append(f"{rel_path}: No OLD/NEW pairs found")
        continue
        
    for old, new in pairs:
        count = new_content.count(old)
        if count == 1:
            new_content = new_content.replace(old, new, 1)
            print(f"[OK] {rel_path}: Replaced 1 instance")
        elif count == 0:
            if new in new_content:
                print(f"[SKIP] {rel_path}: Already applied")
            else:
                errors.append(f"{rel_path}: OLD not found, NEW not present")
        else:
            errors.append(f"{rel_path}: OLD found {count} times (not unique)")
            
    if new_content != content:
        planned.append((rel_path, new_content))

if errors:
    for e in errors:
        print(f"[ERROR] {e}")
    sys.exit(1)

for rel_path, new_content in planned:
    with open(rel_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[WRITE] {rel_path}")

# 執行成功後重置
with open(patch_file, "w", encoding="utf-8") as f:
    f.write("# 請在此貼上新的替換指令\n")
print("[RESET] PATCH.md reset")