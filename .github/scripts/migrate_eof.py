import os
import re
import sys
import subprocess

MODE = os.environ.get("MIGRATE_MODE", "report").lower()
if MODE not in ("report", "apply"):
    print(f"[ERROR] Invalid MIGRATE_MODE: {MODE} (expected 'report' or 'apply')")
    sys.exit(1)

ROOT = os.getcwd()
B_PATTERN = re.compile(r"^B: (.+)$", re.MULTILINE)
B_HISTORY_PREFIX = "B(歷史): "


def find_md_files(base_dir, exclude_dirs=None):
    exclude_dirs = exclude_dirs or [".git", "build-repo", "node_modules"]
    result = []
    if not os.path.isdir(base_dir):
        return result
    for dirpath, dirnames, filenames in os.walk(base_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for fname in filenames:
            if fname.endswith(".md"):
                result.append(os.path.join(dirpath, fname))
    return result


def migrate_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if B_HISTORY_PREFIX in content:
        return ("skip", 0)
    matches = B_PATTERN.findall(content)
    if not matches:
        return ("no_b", 0)
    new_content = B_PATTERN.sub(lambda m: f"B(歷史): {m.group(1)}", content)
    if MODE == "apply":
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        return ("applied", len(matches))
    return ("would_apply", len(matches))


def push_repo(repo_path):
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        print(f"[WARN] {repo_path} 不是 git 倉庫，跳過 push")
        return
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], cwd=repo_path, check=False)
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], cwd=repo_path, check=False)
    subprocess.run(["git", "add", "-A"], cwd=repo_path, check=False)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo_path)
    if diff.returncode != 0:
        subprocess.run(["git", "commit", "-m", "chore: migrate EOF B -> B(歷史)"], cwd=repo_path, check=False)
        push = subprocess.run(["git", "push"], cwd=repo_path, check=False)
        if push.returncode == 0:
            print(f"[PUSH OK] {repo_path}")
        else:
            print(f"[PUSH FAIL] {repo_path}")
    else:
        print(f"[NO CHANGE] {repo_path}")


def main():
    print(f"=== migrate_eof.py (mode={MODE}) ===")
    if MODE == "report":
        print("=== 報告模式：只列清單，不寫入、不推送 ===")

    # 1. AI-General 本倉
    general_files = []
    for d in ["docs", ".github"]:
        general_files.extend(find_md_files(os.path.join(ROOT, d)))

    general_applied = 0
    for f in general_files:
        rel = os.path.relpath(f, ROOT)
        status, count = migrate_file(f)
        if status in ("applied", "would_apply"):
            print(f"[{status.upper()}] {rel} ({count} 處)")
            general_applied += 1
    print(f"[AI-General] 變更 {general_applied} 檔")

    # 2. external/*/
    external_root = os.path.join(ROOT, "external")
    if os.path.isdir(external_root):
        for repo_name in sorted(os.listdir(external_root)):
            repo_path = os.path.join(external_root, repo_name)
            if not os.path.isdir(repo_path):
                continue
            repo_files = find_md_files(repo_path)
            applied = 0
            for f in repo_files:
                rel = os.path.relpath(f, ROOT)
                status, count = migrate_file(f)
                if status in ("applied", "would_apply"):
                    print(f"[{status.upper()}] {rel} ({count} 處)")
                    applied += 1
            print(f"[external/{repo_name}] 變更 {applied} 檔")
            if MODE == "apply" and applied > 0:
                push_repo(repo_path)

    print("=== 完成 ===")


if __name__ == "__main__":
    main()