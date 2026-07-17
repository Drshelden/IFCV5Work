"""
sync_to_gdrive.py
-----------------
Converts .md files in work/ to Google Docs and pushes them to Google Drive.
Mirrors the folder structure under a root Drive folder.

First run: creates Google Docs and records their IDs in drive_index.json.
Subsequent runs: updates existing docs in-place (no duplicates).

Requirements:
    pip install google-api-python-client google-auth --break-system-packages
    Pandoc must be installed: https://pandoc.org/installing.html

Usage:
    python sync_to_gdrive.py [--dry-run]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR   = Path(__file__).resolve().parent
WORK_DIR     = SCRIPT_DIR.parent
INDEX_FILE   = SCRIPT_DIR / "drive_index.json"
SA_FILE      = SCRIPT_DIR / "service_account.json"

ROOT_FOLDER_ID = "1U9J-6hAr5pM_Q28JChDcistHsAHgi33y"

SYNC_FOLDERS = [
    "00 Architecture Overview",
    "01 Decision Register",
    "02 RFCs",
]

ALLOWED_EXTENSIONS = {".md"}

GDOC_MIME   = "application/vnd.google-apps.document"
DOCX_MIME   = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def resolve_pandoc_bin():
    """Return a runnable pandoc executable path/name."""
    for candidate in ("pandoc", "pandoc.exe"):
        found = shutil.which(candidate)
        if found:
            return found

    localappdata = os.environ.get("LOCALAPPDATA")
    manual_candidates = []
    if localappdata:
        manual_candidates.append(Path(localappdata) / "Pandoc" / "pandoc.exe")
    manual_candidates.extend([
        Path("C:/Program Files/Pandoc/pandoc.exe"),
        Path("C:/Program Files (x86)/Pandoc/pandoc.exe"),
    ])

    for candidate in manual_candidates:
        if candidate.exists():
            return str(candidate)

    return None

# ── Auth ───────────────────────────────────────────────────────────────────────

def get_drive_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    if not SA_FILE.exists():
        print(f"ERROR: service_account.json not found at {SA_FILE}")
        print("Download it from Google Cloud Console → IAM → Service Accounts → Keys")
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(
        str(SA_FILE),
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    return build("drive", "v3", credentials=creds, cache_discovery=False)

# ── Drive helpers ──────────────────────────────────────────────────────────────

def get_or_create_folder(service, name, parent_id):
    """Return the Drive folder ID for `name` inside `parent_id`, creating if needed."""
    q = (
        f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
        f" and '{parent_id}' in parents and trashed=false"
    )
    results = service.files().list(q=q, fields="files(id,name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]

    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = service.files().create(body=meta, fields="id").execute()
    print(f"  [FOLDER] Created '{name}'")
    return folder["id"]


def md_to_docx_bytes(md_path, pandoc_bin):
    """Convert a markdown file to .docx bytes using Pandoc."""
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [pandoc_bin, str(md_path), "-o", tmp_path,
             "--from", "markdown", "--to", "docx"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Pandoc error: {result.stderr}")
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def create_gdoc(service, name, docx_bytes, parent_id):
    """Upload docx_bytes as a new Google Doc in parent_id. Returns file ID."""
    from googleapiclient.http import MediaInMemoryUpload

    media = MediaInMemoryUpload(docx_bytes, mimetype=DOCX_MIME, resumable=False)
    meta = {"name": name, "mimeType": GDOC_MIME, "parents": [parent_id]}
    result = service.files().create(
        body=meta,
        media_body=media,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return result["id"]


def update_gdoc(service, file_id, docx_bytes):
    """Replace the content of an existing Google Doc."""
    from googleapiclient.http import MediaInMemoryUpload

    media = MediaInMemoryUpload(docx_bytes, mimetype=DOCX_MIME, resumable=False)
    service.files().update(
        fileId=file_id,
        media_body=media,
        supportsAllDrives=True,
    ).execute()

# ── Index helpers ──────────────────────────────────────────────────────────────

def load_index():
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    return {}


def save_index(index):
    INDEX_FILE.write_text(json.dumps(index, indent=2), encoding="utf-8")

# ── Main sync ──────────────────────────────────────────────────────────────────

def sync_file(service, md_path, folder_id, index, dry_run, pandoc_bin):
    """Sync one .md file to Google Drive as a Google Doc."""
    rel_key = str(md_path.relative_to(WORK_DIR))
    doc_name = md_path.stem  # filename without .md

    try:
        docx_bytes = md_to_docx_bytes(md_path, pandoc_bin)
    except Exception as e:
        print(f"  [ERROR] Pandoc failed for {md_path.name}: {e}")
        return

    if rel_key in index:
        file_id = index[rel_key]
        if not dry_run:
            update_gdoc(service, file_id, docx_bytes)
        print(f"  [UPDATE] {md_path.name}")
    else:
        if not dry_run:
            file_id = create_gdoc(service, doc_name, docx_bytes, folder_id)
            index[rel_key] = file_id
        print(f"  [CREATE] {md_path.name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making changes")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN — no changes will be made ===\n")

    # Verify pandoc is available
    pandoc_bin = resolve_pandoc_bin()
    if not pandoc_bin:
        print("ERROR: pandoc not found. Install from https://pandoc.org/installing.html")
        sys.exit(1)
    try:
        subprocess.run([pandoc_bin, "--version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("ERROR: pandoc was found but failed to run.")
        sys.exit(1)

    service = get_drive_service()
    index   = load_index()

    for folder_name in SYNC_FOLDERS:
        src_dir = WORK_DIR / folder_name
        if not src_dir.exists():
            print(f"  [SKIP] {folder_name} — not found locally")
            continue

        print(f"\n{folder_name}")
        drive_folder_id = get_or_create_folder(service, folder_name, ROOT_FOLDER_ID)

        for md_path in sorted(src_dir.glob("*.md")):
            sync_file(service, md_path, drive_folder_id, index, dry_run=args.dry_run, pandoc_bin=pandoc_bin)

    if not args.dry_run:
        save_index(index)
        print(f"\n✓ drive_index.json updated ({len(index)} entries)")
    else:
        print("\n✓ Dry run complete — no files changed")


if __name__ == "__main__":
    sys.exit(main())
