"""
sync_to_drive.py
----------------
Syncs IFC5 architecture docs (folders 00–02) from work\ to drive-sync\.

Usage:
    python sync_to_drive.py [--dry-run]

What it copies:
    work\00 Architecture Overview\  →  drive-sync\00 Architecture Overview\
    work\01 Decision Register\      →  drive-sync\01 Decision Register\
    work\02 RFCs\                   →  drive-sync\02 RFCs\

File types synced: .md  .csv
All other file types are skipped (e.g. desktop.ini, .xlsx, images).

The script is additive + update-in-place; it does NOT delete files from drive-sync
that are absent from work.  This prevents accidental removal of files added
directly in Google Drive.
"""

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent          # work\scripts\
WORK_DIR   = SCRIPT_DIR.parent                        # work\
ROOT_DIR   = WORK_DIR.parent                          # IFCV5\
DRIVE_SYNC = ROOT_DIR / "drive-sync"

SYNC_FOLDERS = [
    "00 Architecture Overview",
    "01 Decision Register",
    "02 RFCs",
]

ALLOWED_EXTENSIONS = {".md", ".csv"}

# ── Helpers ────────────────────────────────────────────────────────────────────

def file_hash(path: Path) -> str:
    """MD5 of file contents — used to skip identical files."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sync_folder(src: Path, dst: Path, dry_run: bool) -> tuple[int, int]:
    """
    Recursively sync src → dst for allowed extensions.
    Returns (copied, skipped) counts.
    """
    copied = skipped = 0
    for src_file in src.rglob("*"):
        if not src_file.is_file():
            continue
        if src_file.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        rel      = src_file.relative_to(src)
        dst_file = dst / rel

        # Skip if destination is identical
        if dst_file.exists() and file_hash(src_file) == file_hash(dst_file):
            skipped += 1
            continue

        action = "COPY" if not dst_file.exists() else "UPDATE"
        print(f"  [{action}] {rel}")

        if not dry_run:
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_file, dst_file)

        copied += 1

    return copied, skipped


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Sync IFC5 docs to drive-sync folder.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be copied without copying.")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN — no files will be written ===\n")

    if not DRIVE_SYNC.exists():
        print(f"Creating {DRIVE_SYNC}")
        if not args.dry_run:
            DRIVE_SYNC.mkdir(parents=True)

    total_copied = total_skipped = 0

    for folder_name in SYNC_FOLDERS:
        src = WORK_DIR / folder_name
        dst = DRIVE_SYNC / folder_name

        if not src.exists():
            print(f"[WARN] Source folder not found, skipping: {src}")
            continue

        print(f"\n{folder_name}/")
        c, s = sync_folder(src, dst, dry_run=args.dry_run)
        total_copied  += c
        total_skipped += s

    print(f"\n✓ Done — {total_copied} file(s) {'would be ' if args.dry_run else ''}synced, {total_skipped} unchanged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
