"""
sync_to_github.py
-----------------
Stages, commits, and pushes IFC5 architecture docs from work\ to the
Git repo at repo\.

Usage:
    python sync_to_github.py [--message "commit message"] [--dry-run]

What it syncs:
    Folders 00–02 under work\ (.md and .csv only), mirroring the same
    subfolder structure directly into the repo root.

    Excluded: docs\, scripts\, and any other top-level folders.

Repo: https://github.com/Drshelden/IFCV5Work

The script copies matching files into repo\ (mirroring work\ structure),
then runs:
    git add -A
    git commit -m "<message>"
    git push

Prerequisites:
    - repo\ must already be a git repo (git clone it first)
    - Git must be on PATH
    - Remote origin must be authenticated (SSH key or credential helper)

Typical one-time setup:
    cd C:\\_LOCAL\\Claude\\IFCV5\\repo
    git clone https://github.com/Drshelden/IFCV5Work.git .
"""

import argparse
import hashlib
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent          # work\scripts\
WORK_DIR   = SCRIPT_DIR.parent                        # work\
ROOT_DIR   = WORK_DIR.parent                          # IFCV5\
REPO_DIR   = ROOT_DIR / "repo"

REPO_URL = "https://github.com/Drshelden/IFCV5Work.git"

ALLOWED_EXTENSIONS = {".md", ".csv"}

# Only these top-level folders are synced; everything else (docs, scripts, etc.) is excluded
SYNC_FOLDERS = [
    "00 Architecture Overview",
    "01 Decision Register",
    "02 RFCs",
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def file_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path, dry_run: bool) -> subprocess.CompletedProcess | None:
    print(f"  $ {' '.join(cmd)}")
    if dry_run:
        return None
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        print(f"  [ERROR] {result.stderr.strip()}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


def copy_to_repo(dry_run: bool) -> int:
    """
    Copy eligible files from work\<folder>\ directly into repo\<folder>\.
    Returns count of files copied/updated.
    """
    copied = 0

    for folder_name in SYNC_FOLDERS:
        src_root = WORK_DIR / folder_name
        dst_root = REPO_DIR / folder_name

        if not src_root.exists():
            print(f"  [WARN] Source folder not found, skipping: {src_root}")
            continue

        for src_file in src_root.rglob("*"):
            if not src_file.is_file():
                continue
            if src_file.suffix.lower() not in ALLOWED_EXTENSIONS:
                continue

            rel      = src_file.relative_to(src_root)
            dst_file = dst_root / rel

            if dst_file.exists() and file_hash(src_file) == file_hash(dst_file):
                continue  # unchanged

            action = "COPY" if not dst_file.exists() else "UPDATE"
            print(f"  [{action}] {folder_name}/{rel}")

            if not dry_run:
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)

            copied += 1

    return copied


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Sync IFC5 work docs to GitHub repo.")
    parser.add_argument(
        "--message", "-m",
        default=f"docs: sync RFC and decision register {datetime.now().strftime('%Y-%m-%d')}",
        help="Git commit message.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without doing it.")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN — no files will be written or committed ===\n")

    # Validate repo
    if not (REPO_DIR / ".git").exists():
        print(
            f"[ERROR] {REPO_DIR} is not a git repository.\n"
            "Clone the repo first:\n"
            f"  cd {REPO_DIR}\n"
            f"  git clone {REPO_URL} .",
            file=sys.stderr,
        )
        return 1

    # Copy files
    print("Copying files to repo…")
    n = copy_to_repo(dry_run=args.dry_run)
    print(f"  {n} file(s) {'would be ' if args.dry_run else ''}updated.\n")

    # Git operations
    print("Running git…")
    run(["git", "add", "-A"], cwd=REPO_DIR, dry_run=args.dry_run)
    run(["git", "commit", "-m", args.message], cwd=REPO_DIR, dry_run=args.dry_run)
    run(["git", "push"], cwd=REPO_DIR, dry_run=args.dry_run)

    print("\n✓ Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
