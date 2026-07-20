"""
add_new_rfcs.py
---------------
The single script for adding new RFC(s) to the IFC5 project. Run this BEFORE
sync_and_push.bat — it completes everything the RFC needs before any git push.

For each RFC .md file, this script:
  1. Creates a Google Form (feedback form) in the Drive forms/ folder
  2. Uploads the RFC as a Google Doc in the Drive 02 RFCs/ folder
  3. Patches the nav/form blocks in the .md with live URLs (form + doc links)
  4. Re-uploads the patched .md to Drive so the Doc has the correct nav
  5. Appends the RFC to all relevant Python scripts:
       update_rfc_forms.py, rebuild_rfc_headers.py,
       update_priority_form.py, rebuild_rfc_index.py
  6. Regenerates 02 RFCs/README.md (and uploads new version to Drive)
  7. Updates docs/RFC-Sprint-Plan.md and uploads it to Drive
  8. Copies all changed files to repo/ and runs git commit + push

Correct workflow for adding a new RFC:
    1. Write the RFC .md in work/02 RFCs/
    2. python add_new_rfcs.py RFC-IFC5-NNN-*.md
    3. That's it. Do NOT run sync_and_push.bat separately — this script handles
       the git push and Drive sync for the changed files only.

To fix an RFC that was pushed with PENDING nav (e.g. after running sync_and_push
before this script), use --sync-only to redo the Drive/nav/push steps:
    python add_new_rfcs.py RFC-IFC5-041-*.md --sync-only

Usage:
    python add_new_rfcs.py <RFC-IFC5-NNN-*.md> [<more.md> ...] [options]

Options:
    --sprint N      Force sprint assignment (default: auto from tier)
    --dry-run       Show what would happen without making any changes
    --md-only       Skip all Google API calls and git push; patch local files only
    --sync-only     Skip form creation and script patching; just upload to Drive,
                    patch nav, regenerate README, and push. Use to fix a previously
                    pushed RFC that is missing nav links or Drive doc.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
# The script may be run from either work\scripts\ or repo\scripts\.
# PROJECT_ROOT is always the grandparent of whichever scripts\ we're in.

SCRIPT_DIR   = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent   # C:\_LOCAL\Claude\IFCV5\
WORK_DIR     = PROJECT_ROOT / "work"
RFC_DIR      = WORK_DIR / "02 RFCs"
REPO_DIR     = PROJECT_ROOT / "repo"
# Auth/index files always live in work\scripts\ (the authoritative copy)
WORK_SCRIPTS = WORK_DIR / "scripts"
FORMS_INDEX  = WORK_SCRIPTS / "forms_index.json"
DRIVE_INDEX  = WORK_SCRIPTS / "drive_index.json"
OAUTH_FILE   = WORK_SCRIPTS / "oauth_client_secret.json"
TOKEN_FILE   = WORK_SCRIPTS / "oauth_token.json"
SPRINT_PLAN  = WORK_DIR / "docs" / "RFC-Sprint-Plan.md"

REPO_URL       = "https://github.com/Drshelden/IFCV5Work"
ROOT_FOLDER_ID = "1U9J-6hAr5pM_Q28JChDcistHsAHgi33y"  # Drive root for project

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body",
]

GDOC_MIME = "application/vnd.google-apps.document"
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

# Default sprint per tier
TIER_TO_SPRINT = {
    "-tier-1-foundational":       1,
    "-tier-2-core-architecture":  4,
    "-tier-3-domain-modeling":    7,
    "-tier-4-governance":         9,
}

ENCODED_BODY = urllib.parse.quote(
    "**Comment type:** Editorial | Technical Defect | Semantic Concern | "
    "Compatibility Concern | Alternative Proposal | Evidence | "
    "Blocking Objection | General Support\n\n*(delete all but one)*\n\n---\n\n"
    "**Feedback:**\n\n<!-- Be specific — reference section numbers or quote RFC text -->"
    "\n\n---\n\n**Supporting evidence or examples:**\n\n"
    "<!-- Optional: links, code, schema examples, prior art -->"
    "\n\n---\n\n**Questions for the working group:**\n\n"
    "<!-- Optional: number each question Q1, Q2, ... -->\n",
    safe=""
)


# ── RFC metadata extraction ────────────────────────────────────────────────────

def extract_rfc_id(md_path):
    m = re.search(r'RFC-(IFC5-\d+)-', md_path.name)
    if m:
        return m.group(1)
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'\*\*Decision ID\*\*\s*\|\s*(IFC5-\d+)', text)
    if m:
        return m.group(1)
    raise ValueError(f"Cannot extract RFC ID from {md_path.name}")


def extract_title(md_path):
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# RFC"):
            parts = line.split(":", 1)
            return parts[1].strip() if len(parts) > 1 else line.strip()
    return md_path.stem


def extract_tier_slug(md_path):
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'\*\*Tier\*\*\s*\|\s*(\d+)', text)
    if m:
        mapping = {
            "1": "-tier-1-foundational",
            "2": "-tier-2-core-architecture",
            "3": "-tier-3-domain-modeling",
            "4": "-tier-4-governance",
        }
        return mapping.get(m.group(1), "-tier-1-foundational")
    return "-tier-1-foundational"


def extract_prototype_required(md_path):
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'\*\*Prototype Required\*\*\s*\|\s*(Yes|No)', text, re.IGNORECASE)
    return bool(m and m.group(1).strip().lower() == "yes")


def extract_approaches(md_path):
    text = md_path.read_text(encoding="utf-8")
    section = re.search(
        r'##\s+\d*\.?\s*Proposed Approaches?\s*\n(.*?)(?=\n##\s|\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if not section:
        return []
    return [a.strip() for a in re.findall(r'###\s+[\d.]+\s+(.+)', section.group(1))]


def extract_questions(md_path):
    text = md_path.read_text(encoding="utf-8")
    section = re.search(
        r'##\s+\d*\.?\s*Open Questions\s*\n(.*?)(?=\n##\s|\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if not section:
        return []
    questions = re.findall(
        r'\*{0,2}Q(\d+)\.\*{0,2}\s+(.+?)(?=\n\*{0,2}Q\d+\.|\Z)',
        section.group(1), re.DOTALL
    )
    return [(f"Q{n}", t.strip().replace("\n", " ")) for n, t in questions]


# ── Google Auth ───────────────────────────────────────────────────────────────

def get_services(need_forms=True):
    """
    Authenticate and return (forms_svc, drive_svc).
    Pass need_forms=False to request only Drive scope (avoids scope mismatch
    when the cached token was issued without forms.body, e.g. in --sync-only mode).
    If the token has insufficient scope, it is deleted and re-auth is triggered.
    """
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    scopes = SCOPES if need_forms else [SCOPES[0]]  # SCOPES[0] = drive scope

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), scopes)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                # Scope mismatch or revoked token — delete and re-auth
                print("  Token refresh failed (likely scope mismatch). Re-authenticating...")
                TOKEN_FILE.unlink(missing_ok=True)
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_FILE), scopes)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    forms_svc = build("forms", "v1", credentials=creds, cache_discovery=False) if need_forms else None
    drive_svc = build("drive", "v3", credentials=creds, cache_discovery=False)
    return forms_svc, drive_svc


# ── Drive helpers ─────────────────────────────────────────────────────────────

def get_or_create_folder(drive_svc, name, parent_id):
    """Return the Drive folder ID for `name` under `parent_id`, creating if needed."""
    q = (f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
         f" and '{parent_id}' in parents and trashed=false")
    results = drive_svc.files().list(q=q, fields="files(id,name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    folder = drive_svc.files().create(body=meta, fields="id").execute()
    print(f"  [FOLDER] Created '{name}' on Drive")
    return folder["id"]


def find_forms_folder(drive_svc, forms_index):
    """Detect the Drive folder that contains existing forms."""
    if not forms_index:
        return None
    sample = next(iter(forms_index.values()), {})
    form_id = sample.get("id") if isinstance(sample, dict) else None
    if not form_id:
        return None
    try:
        meta = drive_svc.files().get(fileId=form_id, fields="parents", supportsAllDrives=True).execute()
        parents = meta.get("parents", [])
        return parents[0] if parents else None
    except Exception as e:
        print(f"  WARNING: Could not auto-detect forms folder: {e}")
        return None


def resolve_pandoc():
    for candidate in ("pandoc", "pandoc.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    for p in [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe",
        Path("C:/Program Files/Pandoc/pandoc.exe"),
    ]:
        if p.exists():
            return str(p)
    return None


def md_to_docx_bytes(md_path, pandoc_bin):
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            [pandoc_bin, str(md_path), "-o", tmp_path, "--from", "markdown", "--to", "docx"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Pandoc error: {result.stderr}")
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def upload_gdoc(drive_svc, name, docx_bytes, folder_id, existing_id=None):
    """Create or update a Google Doc. Returns file ID."""
    from googleapiclient.http import MediaInMemoryUpload
    media = MediaInMemoryUpload(docx_bytes, mimetype=DOCX_MIME, resumable=False)
    if existing_id:
        drive_svc.files().update(
            fileId=existing_id, media_body=media, supportsAllDrives=True
        ).execute()
        return existing_id
    else:
        meta = {"name": name, "mimeType": GDOC_MIME, "parents": [folder_id]}
        result = drive_svc.files().create(
            body=meta, media_body=media, fields="id", supportsAllDrives=True
        ).execute()
        return result["id"]


def upload_md_to_drive(drive_svc, md_path, drive_folder_name, pandoc_bin, drive_index):
    """
    Convert an .md file to a Google Doc and upload (create or update).
    Updates drive_index in place and saves it. Returns the Google Doc URL or None.
    """
    if not pandoc_bin:
        print(f"  WARNING: Pandoc not found — skipping Drive upload of {md_path.name}")
        return None

    drive_key = f"{drive_folder_name}\\{md_path.name}"
    folder_id = get_or_create_folder(drive_svc, drive_folder_name, ROOT_FOLDER_ID)
    existing_id = drive_index.get(drive_key) or drive_index.get(drive_key.replace("\\", "/"))

    try:
        docx_bytes = md_to_docx_bytes(md_path, pandoc_bin)
        doc_id = upload_gdoc(drive_svc, md_path.stem, docx_bytes, folder_id, existing_id)
        drive_index[drive_key] = doc_id
        DRIVE_INDEX.write_text(json.dumps(drive_index, indent=2), encoding="utf-8")
        action = "UPDATE" if existing_id else "CREATE"
        url = f"https://docs.google.com/document/d/{doc_id}/edit"
        print(f"  [DOC {action}] {md_path.name} → {url}")
        return url
    except Exception as e:
        print(f"  ERROR uploading {md_path.name} to Drive: {e}")
        return None


# ── Nav block patching ─────────────────────────────────────────────────────────

def nav_block_content(rfc_id, slug, tier_slug, form_url, gdoc_url):
    """Build the nav line and form line strings."""
    gh_url   = f"{REPO_URL}/blob/master/02%20RFCs/{slug}.md"
    view_url = f"{REPO_URL}/discussions?discussions_q=label%3A{rfc_id}"
    new_url  = (
        f"{REPO_URL}/discussions/new"
        f"?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}&body={ENCODED_BODY}"
    )
    doc_part = f"[📝 Google Doc]({gdoc_url}) · " if gdoc_url else ""
    nav_line = (
        f"[📄 GitHub MD]({gh_url}) · {doc_part}"
        f"[💬 View all discussions]({view_url}) · "
        f"[+ New discussion]({new_url}) · "
        f"[📋 Take the feedback form]({form_url})"
    )
    form_line = (
        f"📋 **[Take the feedback form for {rfc_id}]({form_url})** "
        f"— answer the open questions and leave comments directly."
    )
    return nav_line, form_line


def patch_nav_block(md_path, rfc_id, slug, tier_slug, form_url, gdoc_url):
    """Replace PENDING placeholders (or old nav) with live URLs."""
    text = md_path.read_text(encoding="utf-8")
    nav_line, form_line = nav_block_content(rfc_id, slug, tier_slug, form_url, gdoc_url)

    # Patch rfc-form block
    text = re.sub(
        r'(<!-- rfc-form -->\n).*?(\n<!-- rfc-nav -->)',
        lambda m: m.group(1) + form_line + m.group(2),
        text, flags=re.DOTALL
    )
    # Patch both rfc-nav lines (header and footer)
    text = re.sub(
        r'(<!-- rfc-nav -->\n)[^\n]+',
        lambda m: m.group(1) + nav_line,
        text
    )

    md_path.write_text(text, encoding="utf-8")
    print(f"  [NAV PATCH] {md_path.name}")


# ── Google Form creation ──────────────────────────────────────────────────────

def create_google_form(forms_svc, drive_svc, rfc_id, slug, tier_slug, title,
                       approaches, questions, forms_folder_id, dry_run):
    if dry_run:
        print(f"  [DRY] Would create form for {rfc_id}")
        return None

    form = forms_svc.forms().create(
        body={"info": {"title": f"{rfc_id} Feedback Form"}}
    ).execute()
    form_id       = form["formId"]
    responder_url = form["responderUri"]

    # Move to forms folder in Drive
    meta = drive_svc.files().get(fileId=form_id, fields="parents", supportsAllDrives=True).execute()
    old_parents = ",".join(meta.get("parents", []))
    drive_svc.files().update(
        fileId=form_id, addParents=forms_folder_id,
        removeParents=old_parents, supportsAllDrives=True,
    ).execute()

    new_disc_url = (
        f"{REPO_URL}/discussions/new?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}&body={ENCODED_BODY}"
    )
    links_text = (
        f"📄 GitHub MD: {REPO_URL}/blob/master/02%20RFCs/{slug}.md\n"
        f"💬 View all discussions: {REPO_URL}/discussions?discussions_q=label%3A{rfc_id}\n"
        f"+ New discussion: {new_disc_url}\n"
        f"📋 Take this feedback form: {responder_url}"
    )

    requests = [
        {"updateSettings": {
            "settings": {"emailCollectionType": "VERIFIED"},
            "updateMask": "emailCollectionType"
        }},
        {"updateFormInfo": {
            "info": {
                "title": f"{rfc_id} Feedback Form",
                "description": (
                    f"Structured feedback form for {rfc_id} — {title}. "
                    "Your email is collected so you can receive a copy of your responses."
                ),
            },
            "updateMask": "title,description"
        }},
    ]

    idx = 0
    items = []

    # General comments
    items.append({"createItem": {"item": {
        "title": "General comments on this RFC",
        "description": "Overall feedback, concerns, or support. Leave blank if you have none.",
        "questionItem": {"question": {"required": False, "textQuestion": {"paragraph": True}}},
    }, "location": {"index": idx}}})
    idx += 1

    # Approach rating grid
    if approaches:
        items.append({"createItem": {"item": {
            "title": "Rate each proposed approach",
            "description": "++ = strongly support  |  + = support  |  0 = no strong view (default)  |  - = oppose",
            "questionGroupItem": {
                "questions": [{"rowQuestion": {"title": a}} for a in approaches],
                "grid": {
                    "columns": {
                        "type": "RADIO",
                        "options": [{"value": "++"}, {"value": "+"}, {"value": "0"}, {"value": "-"}],
                    },
                    "shuffleQuestions": False,
                },
            },
        }, "location": {"index": idx}}})
        idx += 1

    # Individual open questions
    for q_label, q_text in questions:
        items.append({"createItem": {"item": {
            "title": f"{q_label}. {q_text}",
            "questionItem": {"question": {"required": False, "textQuestion": {"paragraph": True}}},
        }, "location": {"index": idx}}})
        idx += 1

    # Links section
    items.append({"createItem": {"item": {
        "title": "Links for this RFC",
        "description": links_text,
        "textItem": {},
    }, "location": {"index": idx}}})

    forms_svc.forms().batchUpdate(
        formId=form_id, body={"requests": requests + items}
    ).execute()

    return {
        "id": form_id,
        "url": responder_url,
        "edit": f"https://docs.google.com/forms/d/{form_id}/edit",
    }


# ── Script file patching ───────────────────────────────────────────────────────

def append_to_rfcs_list(script_path, rfc_id, slug, tier_slug):
    """Append (id, slug, tier_slug) to the RFCS = [...] list in a Python script."""
    text = script_path.read_text(encoding="utf-8")
    if rfc_id in text:
        print(f"  [SKIP] {rfc_id} already in {script_path.name}")
        return
    # Find last 3-tuple entry and the closing ]
    last = re.search(
        r'(\s+\("IFC5-\d+",\s*"[^"]+",\s*"[^"]+"\s*\),?\s*\n)\]',
        text
    )
    if not last:
        print(f"  WARNING: Could not find RFCS 3-tuple list in {script_path.name}")
        return
    new_entry = f'    ("{rfc_id}","{slug}","{tier_slug}"),\n'
    insert_pos = last.start() + len(last.group(1))
    text = text[:insert_pos] + new_entry + text[insert_pos:]
    script_path.write_text(text, encoding="utf-8")
    print(f"  [PATCH] {script_path.name} ← {rfc_id}")


def append_to_priority_rfcs(script_path, rfc_id, title, tier_slug):
    """Append to RFCS and update TIER_GROUPS in update_priority_form.py."""
    text = script_path.read_text(encoding="utf-8")
    if rfc_id in text:
        print(f"  [SKIP] {rfc_id} already in {script_path.name}")
        return

    # 1. Append 2-tuple to RFCS list
    last = re.search(r'(\s+\("IFC5-\d+",\s*"[^"]+"\s*\),?\s*\n)\]', text)
    if last:
        new_entry = f'    ("{rfc_id}", "{title}"),\n'
        insert_pos = last.start() + len(last.group(1))
        text = text[:insert_pos] + new_entry + text[insert_pos:]

    # 2. Find new index and update TIER_GROUPS
    rfcs_section = re.search(r'RFCS\s*=\s*\[(.*?)\]', text, re.DOTALL)
    if rfcs_section:
        rfcs_ids = re.findall(r'"(IFC5-\d+)"', rfcs_section.group(1))
        new_idx = rfcs_ids.index(rfc_id) if rfc_id in rfcs_ids else None
        if new_idx is not None:
            tier_prefix = {
                "-tier-1-foundational":      "Tier 1",
                "-tier-2-core-architecture": "Tier 2",
                "-tier-3-domain-modeling":   "Tier 3",
                "-tier-4-governance":        "Tier 4",
            }.get(tier_slug, "Tier 1")

            def patch_tier_group(m):
                line = m.group(0)
                if tier_prefix in line:
                    # Append [RFCS[N]] before the closing paren+comma
                    line = re.sub(r'\)\s*,\s*$', f' + [RFCS[{new_idx}]],', line)
                return line

            text = re.sub(r'\("Tier \d[^)]+\)', patch_tier_group, text)

    script_path.write_text(text, encoding="utf-8")
    print(f"  [PATCH] {script_path.name} ← {rfc_id}")


def append_to_rfc_index_tier(script_path, rfc_id, slug, title, prototype_required, tier_slug):
    """Append a new RFC tuple to the correct tier's rfcs list in rebuild_rfc_index.py."""
    text = script_path.read_text(encoding="utf-8")
    if rfc_id in text:
        print(f"  [SKIP] {rfc_id} already in {script_path.name}")
        return

    proto_str = "True" if prototype_required else "False"
    new_tuple = f'            ("{rfc_id}","{slug}","{title}",{proto_str}),\n'

    # Find the tier block and its rfcs list
    tier_block = re.search(
        rf'"slug":\s*"{re.escape(tier_slug)}".*?"rfcs":\s*\[(.*?)\],',
        text, re.DOTALL
    )
    if not tier_block:
        print(f"  WARNING: Could not find tier block '{tier_slug}' in {script_path.name}")
        return

    rfcs_start = tier_block.start(1)
    rfcs_text  = text[rfcs_start:tier_block.end(1)]
    last_tuple = list(re.finditer(r'\("IFC5-[^)]+\),?\s*\n', rfcs_text))
    if not last_tuple:
        print(f"  WARNING: No existing tuples in tier block '{tier_slug}'")
        return

    insert_at = rfcs_start + last_tuple[-1].end()
    text = text[:insert_at] + new_tuple + text[insert_at:]
    script_path.write_text(text, encoding="utf-8")
    print(f"  [PATCH] {script_path.name} ← {rfc_id} in {tier_slug}")


def update_rfc_count(script_path, delta=1):
    """
    Increment the RFC count string (e.g. '41 RFCs') in a script by `delta`.
    Only matches standalone counts ≥ 10 to avoid corrupting folder path strings
    like '02 RFCs' that appear in RFC_DIR definitions.
    """
    text = script_path.read_text(encoding="utf-8")
    # Require at least a 2-digit number starting with 1-9 (i.e. 10+) so we
    # never accidentally match the zero-padded folder prefix "02 RFCs".
    m = re.search(r'\b([1-9]\d+) RFCs\b', text)
    if m:
        old_n = int(m.group(1))
        new_n = old_n + delta
        # Use word-boundary replacement to avoid partial matches
        text = re.sub(rf'\b{old_n} RFCs\b', f'{new_n} RFCs', text)
        script_path.write_text(text, encoding="utf-8")
        print(f"  [COUNT] {script_path.name}: {old_n} → {new_n} RFCs")


# ── Sprint plan update ─────────────────────────────────────────────────────────

def update_sprint_plan(sprint_plan_path, rfc_id, title, sprint_num):
    """Add the new RFC to the sprint header line and summary table."""
    text = sprint_plan_path.read_text(encoding="utf-8")
    if rfc_id in text:
        print(f"  [SKIP] {rfc_id} already in sprint plan")
        return

    rfc_num = rfc_id.replace("IFC5-", "")

    # Update **RFCs: NNN, NNN** line
    m = re.search(rf'(### Sprint {sprint_num}[^\n]*\n\*\*RFCs: )([0-9, ]+)(\*\*)', text)
    if m:
        text = text[:m.start(2)] + m.group(2).rstrip(", ") + f", {rfc_num}" + text[m.end(2):]
        print(f"  [SPRINT] Added {rfc_id} to Sprint {sprint_num} header")
    else:
        print(f"  WARNING: Sprint {sprint_num} **RFCs:** line not found in sprint plan")

    # Update summary table row
    m = re.search(rf'(\| {sprint_num} \|[^|]+\| )([^|]+)(\| )', text)
    if m:
        text = text[:m.start(2)] + m.group(2).rstrip() + f", {rfc_num} " + text[m.end(2):]
        print(f"  [SPRINT] Updated summary table row {sprint_num}")

    sprint_plan_path.write_text(text, encoding="utf-8")


# ── Git helpers ───────────────────────────────────────────────────────────────

def copy_to_repo(src_file, repo_subpath):
    """Copy a single file to the repo mirror at repo_subpath."""
    dst = REPO_DIR / repo_subpath
    dst.parent.mkdir(parents=True, exist_ok=True)
    if Path(src_file).resolve() == dst.resolve():
        return  # already in repo (script run from repo\scripts\)
    shutil.copy2(str(src_file), str(dst))


def git_commit_and_push(message):
    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "add", "-A"], check=True)
        result = subprocess.run(["git", "-C", str(REPO_DIR), "diff", "--cached", "--quiet"])
        if result.returncode == 0:
            print("  [GIT] Nothing to commit.")
            return
        subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", message], check=True)
        subprocess.run(["git", "-C", str(REPO_DIR), "push"], check=True)
        print(f"  [GIT] Pushed: {message}")
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: git failed: {e}")


# ── Core per-RFC workflow ─────────────────────────────────────────────────────

def process_rfc(md_path, sprint_override, dry_run, md_only, sync_only,
                forms_svc, drive_svc, forms_index, drive_index, pandoc_bin):
    rfc_id    = extract_rfc_id(md_path)
    slug      = md_path.stem
    title     = extract_title(md_path)
    tier_slug = extract_tier_slug(md_path)
    prototype = extract_prototype_required(md_path)
    sprint    = sprint_override if sprint_override else TIER_TO_SPRINT.get(tier_slug, 1)

    print(f"\n{'='*60}")
    print(f"RFC:    {rfc_id}")
    print(f"Title:  {title}")
    print(f"Tier:   {tier_slug}")
    print(f"Sprint: {sprint}")

    # ── Step 1: Create Google Form ─────────────────────────────────────────────
    form_url = None
    if not md_only and not sync_only:
        if rfc_id in forms_index:
            form_url = forms_index[rfc_id].get("url")
            print(f"  [FORM] Already exists: {form_url}")
        else:
            forms_folder_id = find_forms_folder(drive_svc, forms_index)
            if not forms_folder_id:
                print("  WARNING: Could not detect forms folder — skipping form creation.")
            else:
                approaches = extract_approaches(md_path)
                questions  = extract_questions(md_path)
                print(f"  Approaches: {len(approaches)}, Questions: {len(questions)}")
                result = create_google_form(
                    forms_svc, drive_svc, rfc_id, slug, tier_slug, title,
                    approaches, questions, forms_folder_id, dry_run
                )
                if result and not dry_run:
                    forms_index[rfc_id] = result
                    FORMS_INDEX.write_text(json.dumps(forms_index, indent=2), encoding="utf-8")
                    form_url = result["url"]
                    print(f"  [FORM] Created: {form_url}")
    elif rfc_id in forms_index:
        form_url = forms_index[rfc_id].get("url")
        print(f"  [FORM] {form_url}")

    if not form_url:
        print("  WARNING: No form URL — nav block will not be patched.")

    # ── Step 2: First Drive upload (to get doc ID / URL) ──────────────────────
    gdoc_url = None
    if not md_only and pandoc_bin and not dry_run:
        gdoc_url = upload_md_to_drive(drive_svc, md_path, "02 RFCs", pandoc_bin, drive_index)

    # ── Step 3: Patch nav blocks with form URL + doc URL ──────────────────────
    if form_url and not dry_run:
        patch_nav_block(md_path, rfc_id, slug, tier_slug, form_url, gdoc_url)
    elif dry_run:
        print(f"  [DRY] Would patch nav block in {md_path.name}")

    # ── Step 4: Re-upload patched .md to Drive (so Doc has the correct nav) ───
    if not md_only and pandoc_bin and form_url and not dry_run:
        gdoc_url = upload_md_to_drive(drive_svc, md_path, "02 RFCs", pandoc_bin, drive_index)
        print(f"  [DOC RE-UPLOAD] Nav block now embedded in Drive doc")

    # ── Step 5: Update Python scripts (skip in sync_only mode) ────────────────
    if not sync_only and not dry_run:
        for name, path in [
            ("update_rfc_forms.py",   WORK_SCRIPTS / "update_rfc_forms.py"),
            ("rebuild_rfc_headers.py", WORK_SCRIPTS / "rebuild_rfc_headers.py"),
        ]:
            if path.exists():
                append_to_rfcs_list(path, rfc_id, slug, tier_slug)

        priority_script = WORK_SCRIPTS / "update_priority_form.py"
        if priority_script.exists():
            append_to_priority_rfcs(priority_script, rfc_id, title, tier_slug)

        index_script = WORK_SCRIPTS / "rebuild_rfc_index.py"
        if index_script.exists():
            append_to_rfc_index_tier(index_script, rfc_id, slug, title, prototype, tier_slug)
            update_rfc_count(index_script, delta=1)

    elif dry_run:
        print(f"  [DRY] Would append {rfc_id} to update_rfc_forms.py, rebuild_rfc_headers.py, "
              f"update_priority_form.py, rebuild_rfc_index.py")

    # ── Step 6: Update sprint plan ─────────────────────────────────────────────
    if not dry_run and SPRINT_PLAN.exists():
        update_sprint_plan(SPRINT_PLAN, rfc_id, title, sprint)

    return rfc_id, slug, gdoc_url


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Add new RFC(s) to the IFC5 project — run this BEFORE sync_and_push.bat"
    )
    parser.add_argument("rfcs", nargs="+", help="RFC .md filename(s) in 02 RFCs/ or full paths")
    parser.add_argument("--sprint", type=int, default=None,
                        help="Force sprint assignment (default: auto from tier)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making any changes")
    parser.add_argument("--md-only", action="store_true",
                        help="Skip all Google API calls and git push; patch local files only")
    parser.add_argument("--sync-only", action="store_true",
                        help="Skip form creation and script patching; re-upload to Drive, "
                             "patch nav, regenerate README, and push. Use to fix a previously "
                             "pushed RFC that is missing nav links or Drive doc.")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN — no changes will be made ===\n")
    if args.sync_only:
        print("=== SYNC-ONLY mode — skipping form creation and script patching ===\n")

    # Resolve file paths
    md_paths = []
    for p in args.rfcs:
        path = Path(p)
        if not path.is_absolute():
            path = RFC_DIR / p
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            sys.exit(1)
        md_paths.append(path)

    # Load indexes
    forms_index = json.loads(FORMS_INDEX.read_text(encoding="utf-8")) if FORMS_INDEX.exists() else {}
    drive_index = json.loads(DRIVE_INDEX.read_text(encoding="utf-8")) if DRIVE_INDEX.exists() else {}

    # Google services
    # sync-only mode only needs Drive scope; form creation needs both Drive + Forms
    forms_svc = drive_svc = None
    if not args.md_only and not args.dry_run:
        need_forms = not args.sync_only
        print(f"Authenticating with Google ({'Drive only' if not need_forms else 'Drive + Forms'})...")
        forms_svc, drive_svc = get_services(need_forms=need_forms)

    # Pandoc
    pandoc_bin = resolve_pandoc() if not args.md_only else None
    if not args.md_only and not pandoc_bin:
        print("WARNING: Pandoc not found — Drive doc uploads will be skipped.")

    # Process each RFC
    processed = []
    for md_path in md_paths:
        rfc_id, slug, gdoc_url = process_rfc(
            md_path, args.sprint, args.dry_run, args.md_only, args.sync_only,
            forms_svc, drive_svc, forms_index, drive_index, pandoc_bin
        )
        processed.append((rfc_id, slug))

    if not processed:
        print("\nNo RFCs processed.")
        return

    # ── Regenerate RFC Index README ────────────────────────────────────────────
    if not args.dry_run:
        print("\nRegenerating 02 RFCs/README.md and uploading to Drive...")
        index_script = WORK_SCRIPTS / "rebuild_rfc_index.py"
        flag = ["--md-only"] if args.md_only else []
        subprocess.run([sys.executable, str(index_script)] + flag, check=False)

    # ── Selective Drive upload of sprint plan ──────────────────────────────────
    if not args.md_only and not args.dry_run and SPRINT_PLAN.exists() and drive_svc and pandoc_bin:
        print("\nUploading sprint plan to Drive...")
        upload_md_to_drive(drive_svc, SPRINT_PLAN, "docs", pandoc_bin, drive_index)

    # ── Copy changed files to repo/ and push to GitHub ────────────────────────
    if not args.md_only and not args.dry_run and REPO_DIR.exists():
        print("\nCopying to repo/...")

        # RFC .md files
        for rfc_id, slug in processed:
            md_path = RFC_DIR / f"{slug}.md"
            copy_to_repo(md_path, f"02 RFCs/{slug}.md")

        # RFC README
        readme = RFC_DIR / "README.md"
        if readme.exists():
            copy_to_repo(readme, "02 RFCs/README.md")

        # Sprint plan
        if SPRINT_PLAN.exists():
            copy_to_repo(SPRINT_PLAN, "docs/RFC-Sprint-Plan.md")

        # Updated scripts (only if not sync_only, as scripts weren't changed)
        if not args.sync_only:
            for script_name in [
                "update_rfc_forms.py", "rebuild_rfc_headers.py",
                "update_priority_form.py", "rebuild_rfc_index.py",
                "add_new_rfcs.py",
            ]:
                src = WORK_SCRIPTS / script_name
                if src.exists():
                    copy_to_repo(src, f"scripts/{script_name}")

        # Forms/drive indexes
        for idx_file in [FORMS_INDEX, DRIVE_INDEX]:
            if idx_file.exists():
                copy_to_repo(idx_file, f"scripts/{idx_file.name}")

        # Git push
        rfc_ids = [r for r, _ in processed]
        message = ("Fix" if args.sync_only else "Add") + " RFC(s): " + ", ".join(rfc_ids)
        git_commit_and_push(message)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"Done. Processed: {', '.join(r for r, _ in processed)}")
    if args.dry_run or args.md_only:
        print("\nNext: run without --dry-run / --md-only to push to Drive and GitHub.")
    else:
        print("\nDone. You do NOT need to run sync_and_push.bat for these RFCs.")
        print("sync_and_push.bat is still useful for bulk syncs of modified existing files.")


if __name__ == "__main__":
    sys.exit(main())
