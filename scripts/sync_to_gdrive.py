"""
sync_to_gdrive.py
-----------------
Converts .md files in work/ to Google Docs and pushes them to Google Drive.
Mirrors the folder structure under a root Drive folder.

First run: creates Google Docs and records their IDs in drive_index.json.
Subsequent runs: updates existing docs in-place (no duplicates).

Requirements:
    pip install google-api-python-client google-auth google-auth-oauthlib --break-system-packages
    Pandoc must be installed: https://pandoc.org/installing.html

OAuth setup:
    1) Create an OAuth Desktop App client in Google Cloud Console.
    2) Save the JSON as scripts/oauth_client_secret.json
    3) First run will open a browser for consent and save scripts/oauth_token.json

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
OAUTH_CLIENT_FILE = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE   = SCRIPT_DIR / "oauth_token.json"
SCOPES       = ["https://www.googleapis.com/auth/drive"]

ROOT_FOLDER_ID = "1U9J-6hAr5pM_Q28JChDcistHsAHgi33y"

SYNC_FOLDERS = [
    "00 Architecture Overview",
    "01 Decision Register",
    "02 RFCs",
]

# Folders synced recursively as raw binary files (not converted to Google Docs)
BINARY_SYNC_FOLDERS = [
    "03 Reference Examples",
]

ALLOWED_EXTENSIONS = {".md"}

# Extensions uploaded as raw binary files (not converted to Google Docs)
BINARY_EXTENSIONS = {".ifc", ".ifcx", ".json", ".csv", ".txt", ".xml"}

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
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow

    if not OAUTH_CLIENT_FILE.exists():
        print(f"ERROR: OAuth client JSON not found at {OAUTH_CLIENT_FILE}")
        print("Create a Google OAuth Desktop App client and save its JSON to that path.")
        sys.exit(1)

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_CLIENT_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

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


def guess_mime(path):
    """Return a MIME type for common binary extensions."""
    ext = path.suffix.lower()
    return {
        ".json":  "application/json",
        ".ifc":   "application/octet-stream",
        ".ifcx":  "application/octet-stream",
        ".csv":   "text/csv",
        ".txt":   "text/plain",
        ".xml":   "application/xml",
    }.get(ext, "application/octet-stream")


def create_binary_file(service, name, data, parent_id, mime):
    """Upload raw bytes as a new Drive file (not converted). Returns file ID."""
    from googleapiclient.http import MediaInMemoryUpload

    media = MediaInMemoryUpload(data, mimetype=mime, resumable=False)
    meta  = {"name": name, "parents": [parent_id]}
    result = service.files().create(
        body=meta,
        media_body=media,
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return result["id"]


def update_binary_file(service, file_id, data, mime):
    """Replace content of an existing Drive binary file."""
    from googleapiclient.http import MediaInMemoryUpload

    media = MediaInMemoryUpload(data, mimetype=mime, resumable=False)
    service.files().update(
        fileId=file_id,
        media_body=media,
        supportsAllDrives=True,
    ).execute()


def sync_binary_file(service, file_path, folder_id, index, dry_run):
    """Sync one binary (non-md) file to Google Drive as a raw file."""
    rel_key = str(file_path.relative_to(WORK_DIR))
    mime    = guess_mime(file_path)
    data    = file_path.read_bytes()

    if rel_key in index:
        file_id = index[rel_key]
        if not dry_run:
            update_binary_file(service, file_id, data, mime)
        print(f"  [UPDATE] {file_path.name}")
    else:
        if not dry_run:
            file_id = create_binary_file(service, file_path.name, data, folder_id, mime)
            index[rel_key] = file_id
        print(f"  [CREATE] {file_path.name}")

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

    for folder_name in BINARY_SYNC_FOLDERS:
        src_dir = WORK_DIR / folder_name
        if not src_dir.exists():
            print(f"  [SKIP] {folder_name} — not found locally")
            continue

        print(f"\n{folder_name}")
        root_folder_id = get_or_create_folder(service, folder_name, ROOT_FOLDER_ID)

        # Walk subdirectories recursively
        for file_path in sorted(src_dir.rglob("*")):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in BINARY_EXTENSIONS:
                continue

            # Ensure parent folder exists on Drive
            rel_parts = file_path.relative_to(src_dir).parts
            parent_id = root_folder_id
            for part in rel_parts[:-1]:  # subdirs only, not filename
                parent_id = get_or_create_folder(service, part, parent_id)

            sync_binary_file(service, file_path, parent_id, index, dry_run=args.dry_run)

    if not args.dry_run:
        save_index(index)
        print(f"\n✓ drive_index.json updated ({len(index)} entries)")
    else:
        print("\n✓ Dry run complete — no files changed")


if __name__ == "__main__":
    sys.exit(main())
