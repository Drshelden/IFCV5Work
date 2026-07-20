"""
add_new_rfcs.py
---------------
Adds one or more new RFC .md files to the IFC5 project. For each RFC, this script:
  1. Creates a Google Form (feedback form)
  2. Creates a Google Doc (uploads .md converted via Pandoc)
  3. Patches the nav blocks in the .md file with live URLs
  4. Appends the RFC to all relevant Python scripts:
       - update_rfc_forms.py (RFCS list)
       - rebuild_rfc_headers.py (RFCS list)
       - update_priority_form.py (RFCS list + TIER_GROUPS)
       - rebuild_rfc_index.py (TIERS[tier].rfcs list)
  5. Regenerates 02 RFCs/README.md by calling rebuild_rfc_index.py
  6. Updates docs/RFC-Sprint-Plan.md to include the new RFC
  7. Commits and pushes everything to GitHub
  8. Syncs to Google Drive via sync_to_gdrive.py

Usage:
    python add_new_rfcs.py <path/to/RFC-IFC5-NNN-*.md> [<more.md> ...] [options]

Options:
    --sprint N      Force assignment to sprint N in the sprint plan (default: auto from tier)
    --dry-run       Show what would happen without making Drive/Forms/git changes
    --md-only       Skip all Google API calls and git push; just patch local files
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

SCRIPT_DIR  = Path(__file__).resolve().parent
WORK_DIR    = SCRIPT_DIR.parent
RFC_DIR     = WORK_DIR / "02 RFCs"
REPO_DIR    = WORK_DIR.parent / "repo"
FORMS_INDEX = SCRIPT_DIR / "forms_index.json"
DRIVE_INDEX = SCRIPT_DIR / "drive_index.json"
OAUTH_FILE  = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE  = SCRIPT_DIR / "oauth_token.json"
SPRINT_PLAN = WORK_DIR / "docs" / "RFC-Sprint-Plan.md"

REPO_URL = "https://github.com/Drshelden/IFCV5Work"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body",
]

GDOC_MIME  = "application/vnd.google-apps.document"
DOCX_MIME  = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

# Maps tier slug → default sprint number
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
    "**Feedback:**\n\n<!-- Be specific — reference section numbers or quote RFC text where relevant -->"
    "\n\n---\n\n**Supporting evidence or examples:**\n\n"
    "<!-- Optional: links, code, schema examples, prior art -->"
    "\n\n---\n\n**Questions for the working group:**\n\n"
    "<!-- Optional: number each question Q1, Q2, ... -->\n",
    safe=""
)


# ── RFC metadata extraction ────────────────────────────────────────────────────

def extract_rfc_id(md_path):
    """Extract RFC ID (e.g. IFC5-041) from the filename or content."""
    m = re.search(r'RFC-(IFC5-\d+)-', md_path.name)
    if m:
        return m.group(1)
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'\*\*Decision ID\*\*\s*\|\s*(IFC5-\d+)', text)
    if m:
        return m.group(1)
    raise ValueError(f"Cannot extract RFC ID from {md_path.name}")


def extract_title(md_path):
    """Extract the RFC title (after the colon in the H1 heading)."""
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# RFC"):
            parts = line.split(":", 1)
            return parts[1].strip() if len(parts) > 1 else line.strip()
    return md_path.stem


def extract_tier_slug(md_path):
    """Extract tier slug (e.g. -tier-1-foundational) from the Tier field."""
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'\*\*Tier\*\*\s*\|\s*(\d+)\s*[—–]\s*(\w[\w\s]+)', text)
    if m:
        tier_num = m.group(1)
        label    = m.group(2).strip().lower()
        mapping = {
            "1": "-tier-1-foundational",
            "2": "-tier-2-core-architecture",
            "3": "-tier-3-domain-modeling",
            "4": "-tier-4-governance",
        }
        return mapping.get(tier_num, "-tier-1-foundational")
    return "-tier-1-foundational"


def extract_prototype_required(md_path):
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'\*\*Prototype Required\*\*\s*\|\s*(Yes|No)', text, re.IGNORECASE)
    return m and m.group(1).strip().lower() == "yes" if m else False


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

def get_services():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

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
            flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return (
        build("forms", "v1", credentials=creds, cache_discovery=False),
        build("drive", "v3", credentials=creds, cache_discovery=False),
    )


# ── Drive helpers ──────────────────────────────────────────────────────────────

def get_or_create_folder(drive_svc, name, parent_id):
    q = (f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
         f" and '{parent_id}' in parents and trashed=false")
    results = drive_svc.files().list(q=q, fields="files(id,name)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent_id]}
    folder = drive_svc.files().create(body=meta, fields="id").execute()
    return folder["id"]


def find_forms_folder(drive_svc, forms_index):
    """Auto-detect the Drive folder that existing forms live in."""
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
        print(f"  WARNING: could not auto-detect forms folder: {e}")
        return None


def find_rfc_folder_id(drive_svc):
    """Find the '02 RFCs' folder in Drive (child of root folder)."""
    ROOT_FOLDER_ID = "1U9J-6hAr5pM_Q28JChDcistHsAHgi33y"
    q = (f"name='02 RFCs' and mimeType='application/vnd.google-apps.folder'"
         f" and '{ROOT_FOLDER_ID}' in parents and trashed=false")
    results = drive_svc.files().list(q=q, fields="files(id,name)").execute()
    files = results.get("files", [])
    return files[0]["id"] if files else None


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
            raise RuntimeError(f"Pandoc: {result.stderr}")
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
        drive_svc.files().update(fileId=existing_id, media_body=media, supportsAllDrives=True).execute()
        return existing_id
    else:
        meta = {"name": name, "mimeType": GDOC_MIME, "parents": [folder_id]}
        result = drive_svc.files().create(body=meta, media_body=media, fields="id", supportsAllDrives=True).execute()
        return result["id"]


# ── Form creation ─────────────────────────────────────────────────────────────

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

    # Move to forms folder
    meta = drive_svc.files().get(fileId=form_id, fields="parents", supportsAllDrives=True).execute()
    old_parents = ",".join(meta.get("parents", []))
    drive_svc.files().update(
        fileId=form_id, addParents=forms_folder_id,
        removeParents=old_parents, supportsAllDrives=True,
    ).execute()

    new_disc_url = (
        f"{REPO_URL}/discussions/new"
        f"?category={tier_slug}"
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
        {"updateSettings": {"settings": {"emailCollectionType": "VERIFIED"}, "updateMask": "emailCollectionType"}},
        {"updateFormInfo": {"info": {"title": f"{rfc_id} Feedback Form",
                                     "description": f"Structured feedback form for {rfc_id} — {title}."},
                            "updateMask": "title,description"}},
    ]

    idx   = 0
    items = []

    items.append({"createItem": {"item": {
        "title": "General comments on this RFC",
        "description": "Overall feedback, concerns, or support.",
        "questionItem": {"question": {"required": False, "textQuestion": {"paragraph": True}}},
    }, "location": {"index": idx}}})
    idx += 1

    if approaches:
        items.append({"createItem": {"item": {
            "title": "Rate each proposed approach",
            "description": "++ strongly support | + support | 0 no strong view | - oppose",
            "questionGroupItem": {
                "questions": [{"rowQuestion": {"title": a}} for a in approaches],
                "grid": {"columns": {"type": "RADIO",
                                     "options": [{"value": "++"}, {"value": "+"}, {"value": "0"}, {"value": "-"}]},
                         "shuffleQuestions": False},
            },
        }, "location": {"index": idx}}})
        idx += 1

    for q_label, q_text in questions:
        items.append({"createItem": {"item": {
            "title": f"{q_label}. {q_text}",
            "questionItem": {"question": {"required": False, "textQuestion": {"paragraph": True}}},
        }, "location": {"index": idx}}})
        idx += 1

    items.append({"createItem": {"item": {
        "title": "Links for this RFC",
        "description": links_text,
        "textItem": {},
    }, "location": {"index": idx}}})

    forms_svc.forms().batchUpdate(formId=form_id, body={"requests": requests + items}).execute()

    return {
        "id": form_id,
        "url": responder_url,
        "edit": f"https://docs.google.com/forms/d/{form_id}/edit",
    }


# ── Nav block patching ─────────────────────────────────────────────────────────

def patch_nav_block(md_path, rfc_id, slug, tier_slug, form_url, gdoc_url):
    text = md_path.read_text(encoding="utf-8")
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
    text = re.sub(
        r'(<!-- rfc-form -->\n).*?(\n<!-- rfc-nav -->)',
        lambda m: m.group(1) + form_line + m.group(2),
        text, flags=re.DOTALL
    )
    text = re.sub(r'(<!-- rfc-nav -->\n)[^\n]+', lambda m: m.group(1) + nav_line, text)
    md_path.write_text(text, encoding="utf-8")
    print(f"  [PATCH] {md_path.name}")


# ── Script file patching ───────────────────────────────────────────────────────

def append_to_rfcs_list(script_path, rfc_id, slug, tier_slug):
    """Append a new entry to the RFCS = [...] list in a Python script."""
    text = script_path.read_text(encoding="utf-8")
    # Find the last entry in RFCS before the closing bracket
    # Pattern: find a line with ("IFC5-NNN",...) followed by a line that might close the list
    last_entry = re.search(
        r'(\s+\("IFC5-\d+",\s*"[^"]+",\s*"[^"]+"\s*\),?\s*\n)\]',
        text
    )
    if not last_entry:
        print(f"  WARNING: Could not find RFCS list in {script_path.name}")
        return

    # Build new entry — detect how many columns the existing entries have
    sample = re.search(r'\("IFC5-\d+",\s*("[^"]+"),\s*("[^"]+")\)', text)
    if sample:
        # 3-tuple format: (id, slug, tier_slug)
        new_entry = f'    ("{rfc_id}","{slug}","{tier_slug}"),\n'
    else:
        print(f"  WARNING: unrecognized RFCS format in {script_path.name}")
        return

    insert_pos = last_entry.start() + len(last_entry.group(1))
    text = text[:insert_pos] + new_entry + text[insert_pos:]
    script_path.write_text(text, encoding="utf-8")
    print(f"  [PATCH] {script_path.name} — appended {rfc_id}")


def append_to_priority_rfcs(script_path, rfc_id, title, tier_slug):
    """Append new entry to RFCS list and update TIER_GROUPS in update_priority_form.py."""
    text = script_path.read_text(encoding="utf-8")

    # 1. Append to RFCS = [...] (2-tuple format: (id, title))
    last_2tuple = re.search(
        r'(\s+\("IFC5-\d+",\s*"[^"]+"\s*\),?\s*\n)\]',
        text
    )
    if last_2tuple:
        new_rfc_entry = f'    ("{rfc_id}", "{title}"),\n'
        insert_pos = last_2tuple.start() + len(last_2tuple.group(1))
        text = text[:insert_pos] + new_rfc_entry + text[insert_pos:]
    else:
        print(f"  WARNING: Could not find RFCS 2-tuple list in {script_path.name}")

    # 2. Update TIER_GROUPS — find the right tier group and add [RFCS[new_index]]
    # First count how many RFCS entries exist now (after insertion above)
    all_ids = re.findall(r'"(IFC5-\d+)"', text)
    # Deduplicate preserving order, but only from RFCS list
    rfcs_section = re.search(r'RFCS\s*=\s*\[(.*?)\]', text, re.DOTALL)
    if rfcs_section:
        rfcs_ids = re.findall(r'"(IFC5-\d+)"', rfcs_section.group(1))
        new_idx = rfcs_ids.index(rfc_id) if rfc_id in rfcs_ids else None
        if new_idx is not None:
            tier_label_map = {
                "-tier-1-foundational":      "Tier 1",
                "-tier-2-core-architecture": "Tier 2",
                "-tier-3-domain-modeling":   "Tier 3",
                "-tier-4-governance":        "Tier 4",
            }
            tier_prefix = tier_label_map.get(tier_slug, "Tier 1")

            # Find the tier group entry and append [RFCS[N]] to it
            def patch_tier_group(m):
                line = m.group(0)
                if tier_prefix in line and "TIER_GROUPS" not in line:
                    # Add to the expression before the closing )
                    line = re.sub(r'\)\s*,?\s*$', f' + [RFCS[{new_idx}]],', line)
                return line

            text = re.sub(r'\("Tier \d[^"]*",.*?\)', patch_tier_group, text, flags=re.DOTALL)

    script_path.write_text(text, encoding="utf-8")
    print(f"  [PATCH] {script_path.name} — appended {rfc_id}")


def append_to_rfc_index_tier(script_path, rfc_id, slug, title, prototype_required, tier_slug):
    """Append a new RFC tuple to the correct tier's rfcs list in rebuild_rfc_index.py."""
    text = script_path.read_text(encoding="utf-8")
    proto_str = "True" if prototype_required else "False"
    new_tuple = f'            ("{rfc_id}","{slug}","{title}",{proto_str}),\n'

    # Find the tier block for this tier and insert before its closing ],
    # Tier blocks look like: "slug": "-tier-1-foundational", ... "rfcs": [...],
    tier_block = re.search(
        rf'"slug":\s*"{re.escape(tier_slug)}".*?"rfcs":\s*\[(.*?)\],',
        text, re.DOTALL
    )
    if not tier_block:
        print(f"  WARNING: Could not find tier block {tier_slug} in {script_path.name}")
        return

    # Find the last tuple in that rfcs list
    rfcs_content = tier_block.group(1)
    # Find position of last tuple's end in the overall text
    rfcs_start = tier_block.start(1)
    rfcs_end   = tier_block.end(1)
    rfcs_text  = text[rfcs_start:rfcs_end]

    last_tuple = list(re.finditer(r'\("IFC5-[^)]+\),?\s*\n', rfcs_text))
    if not last_tuple:
        print(f"  WARNING: No existing tuples in {tier_slug} block")
        return

    insert_at = rfcs_start + last_tuple[-1].end()
    text = text[:insert_at] + new_tuple + text[insert_at:]
    script_path.write_text(text, encoding="utf-8")
    print(f"  [PATCH] {script_path.name} — added {rfc_id} to {tier_slug}")


def update_rfc_count_in_script(script_path, old_count, new_count):
    """Update any '38 RFCs' / '40 RFCs' count strings in a script."""
    text = script_path.read_text(encoding="utf-8")
    text = text.replace(f"{old_count} RFCs", f"{new_count} RFCs")
    script_path.write_text(text, encoding="utf-8")


# ── Sprint plan update ─────────────────────────────────────────────────────────

def update_sprint_plan(sprint_plan_path, rfc_id, title, sprint_num, tier_slug):
    """Add the new RFC to the appropriate sprint section and summary table."""
    text = sprint_plan_path.read_text(encoding="utf-8")

    rfc_num = rfc_id.replace("IFC5-", "")  # e.g. "041"

    # 1. Update the **RFCs:** line in the sprint section header
    sprint_section = re.search(
        rf'(### Sprint {sprint_num}[^\n]*\n\*\*RFCs: )([0-9, ]+)(\*\*)',
        text
    )
    if sprint_section:
        existing = sprint_section.group(2).rstrip(", ")
        new_rfcs_line = f"{existing}, {rfc_num}"
        text = text[:sprint_section.start(2)] + new_rfcs_line + text[sprint_section.end(2):]
        print(f"  [SPRINT] Updated Sprint {sprint_num} RFC list")
    else:
        print(f"  WARNING: Could not find Sprint {sprint_num} header in sprint plan")

    # 2. Update summary table — find the row for sprint N and update RFCs column
    table_row = re.search(
        rf'(\| {sprint_num} \|[^|]+\| )([^|]+)(\|[^|]+\|)',
        text
    )
    if table_row:
        existing_cell = table_row.group(2).rstrip()
        new_cell = existing_cell + f", {rfc_num}"
        text = text[:table_row.start(2)] + new_cell + " " + text[table_row.end(2):]
        print(f"  [SPRINT] Updated summary table row {sprint_num}")
    else:
        print(f"  WARNING: Could not find sprint {sprint_num} in summary table")

    # 3. Add a note about the new RFC to the sprint's descriptive paragraph
    # Insert a sentence after the sprint's paragraph, noting the added RFC
    sprint_end = re.search(
        rf'(### Sprint {sprint_num}.*?\n---)',
        text, re.DOTALL
    )
    if sprint_end and rfc_id not in text:
        note = f"\n*Note: {rfc_id} ({title}) was added to this sprint.*\n"
        insert_before = sprint_end.end() - 4  # before '---'
        text = text[:insert_before] + note + text[insert_before:]

    sprint_plan_path.write_text(text, encoding="utf-8")


# ── Git push ──────────────────────────────────────────────────────────────────

def git_commit_and_push(repo_dir, message, dry_run):
    if dry_run:
        print(f"  [DRY] Would git commit: {message}")
        return
    try:
        subprocess.run(["git", "-C", str(repo_dir), "add", "-A"], check=True)
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "diff", "--cached", "--quiet"]
        )
        if result.returncode == 0:
            print("  [GIT] Nothing to commit.")
            return
        subprocess.run(["git", "-C", str(repo_dir), "commit", "-m", message], check=True)
        subprocess.run(["git", "-C", str(repo_dir), "push"], check=True)
        print(f"  [GIT] Pushed: {message}")
    except subprocess.CalledProcessError as e:
        print(f"  ERROR: git failed: {e}")


def robocopy_to_repo(src, dst, flags="*.md"):
    """Copy updated files to the repo mirror."""
    try:
        args = ["robocopy", str(src), str(dst)]
        if flags:
            args += flags.split()
        args += ["/njh", "/njs"]
        subprocess.run(args, check=False)  # robocopy exits nonzero on "files copied"
    except Exception as e:
        print(f"  WARNING: robocopy failed: {e}")


# ── Main ───────────────────────────────────────────────────────────────────────

def process_rfc(md_path, sprint_override, dry_run, md_only, forms_svc, drive_svc,
                forms_index, drive_index, pandoc_bin):
    rfc_id    = extract_rfc_id(md_path)
    slug      = md_path.stem
    title     = extract_title(md_path)
    tier_slug = extract_tier_slug(md_path)
    prototype = extract_prototype_required(md_path)
    sprint    = sprint_override if sprint_override else TIER_TO_SPRINT.get(tier_slug, 1)

    print(f"\n{'='*60}")
    print(f"RFC:   {rfc_id}")
    print(f"Title: {title}")
    print(f"Tier:  {tier_slug}")
    print(f"Sprint: {sprint}")

    # ── 1. Create Google Form ──────────────────────────────────────────────────
    form_url = None
    if not md_only and rfc_id not in forms_index:
        forms_folder_id = find_forms_folder(drive_svc, forms_index)
        if not forms_folder_id:
            print("  WARNING: Could not detect forms folder. Skipping form creation.")
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
                print(f"  [FORM] {result['url']}")
                form_url = result["url"]
    elif rfc_id in forms_index:
        form_url = forms_index[rfc_id].get("url")
        print(f"  [FORM] Already exists: {form_url}")

    # ── 2. Upload Google Doc ──────────────────────────────────────────────────
    gdoc_url = None
    drive_key = f"02 RFCs\\{slug}.md"
    if not md_only and pandoc_bin:
        rfc_folder_id = find_rfc_folder_id(drive_svc)
        if rfc_folder_id:
            try:
                docx_bytes  = md_to_docx_bytes(md_path, pandoc_bin)
                existing_id = drive_index.get(drive_key) or drive_index.get(drive_key.replace("\\", "/"))
                doc_id = upload_gdoc(drive_svc, slug, docx_bytes, rfc_folder_id, existing_id)
                drive_index[drive_key] = doc_id
                DRIVE_INDEX.write_text(json.dumps(drive_index, indent=2), encoding="utf-8")
                gdoc_url = f"https://docs.google.com/document/d/{doc_id}/edit"
                action = "UPDATE" if existing_id else "CREATE"
                print(f"  [DOC {action}] {gdoc_url}")
            except Exception as e:
                print(f"  ERROR: Drive upload failed: {e}")
        else:
            print("  WARNING: Could not find '02 RFCs' Drive folder. Skipping Doc upload.")
    elif drive_key in drive_index:
        gdoc_url = f"https://docs.google.com/document/d/{drive_index[drive_key]}/edit"

    # ── 3. Patch nav blocks ───────────────────────────────────────────────────
    if form_url and not dry_run:
        patch_nav_block(md_path, rfc_id, slug, tier_slug, form_url, gdoc_url)

    # ── 4. Patch Python scripts ───────────────────────────────────────────────
    scripts = {
        "update_rfc_forms.py":   SCRIPT_DIR / "update_rfc_forms.py",
        "rebuild_rfc_headers.py": SCRIPT_DIR / "rebuild_rfc_headers.py",
    }
    for name, path in scripts.items():
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            if rfc_id not in existing:
                if not dry_run:
                    append_to_rfcs_list(path, rfc_id, slug, tier_slug)
                else:
                    print(f"  [DRY] Would append {rfc_id} to {name}")

    priority_script = SCRIPT_DIR / "update_priority_form.py"
    if priority_script.exists():
        existing = priority_script.read_text(encoding="utf-8")
        if rfc_id not in existing:
            if not dry_run:
                append_to_priority_rfcs(priority_script, rfc_id, title, tier_slug)
            else:
                print(f"  [DRY] Would append {rfc_id} to update_priority_form.py")

    index_script = SCRIPT_DIR / "rebuild_rfc_index.py"
    if index_script.exists():
        existing = index_script.read_text(encoding="utf-8")
        if rfc_id not in existing:
            if not dry_run:
                append_to_rfc_index_tier(index_script, rfc_id, slug, title, prototype, tier_slug)
            else:
                print(f"  [DRY] Would add {rfc_id} to rebuild_rfc_index.py")

    # ── 5. Update sprint plan ─────────────────────────────────────────────────
    if SPRINT_PLAN.exists() and not dry_run:
        if rfc_id not in SPRINT_PLAN.read_text(encoding="utf-8"):
            update_sprint_plan(SPRINT_PLAN, rfc_id, title, sprint, tier_slug)
        else:
            print(f"  [SPRINT] {rfc_id} already in sprint plan")

    return rfc_id


def main():
    parser = argparse.ArgumentParser(description="Add new RFC(s) to the IFC5 project")
    parser.add_argument("rfcs", nargs="+", help="Path(s) to RFC .md file(s)")
    parser.add_argument("--sprint", type=int, default=None,
                        help="Force sprint assignment (default: auto from tier)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making changes")
    parser.add_argument("--md-only", action="store_true",
                        help="Skip Google API calls and git push; patch local files only")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN — no changes will be made ===\n")

    # Resolve paths
    md_paths = []
    for p in args.rfcs:
        path = Path(p)
        if not path.is_absolute():
            path = RFC_DIR / path
        if not path.exists():
            print(f"ERROR: File not found: {path}")
            sys.exit(1)
        md_paths.append(path)

    # Load indexes
    forms_index = json.loads(FORMS_INDEX.read_text(encoding="utf-8")) if FORMS_INDEX.exists() else {}
    drive_index = json.loads(DRIVE_INDEX.read_text(encoding="utf-8")) if DRIVE_INDEX.exists() else {}

    # Google services
    forms_svc = drive_svc = None
    if not args.md_only and not args.dry_run:
        print("Authenticating with Google...")
        forms_svc, drive_svc = get_services()

    # Pandoc
    pandoc_bin = None
    if not args.md_only:
        pandoc_bin = resolve_pandoc()
        if not pandoc_bin:
            print("WARNING: Pandoc not found. Google Doc upload will be skipped.")

    # Count existing RFCs for count update
    index_script = SCRIPT_DIR / "rebuild_rfc_index.py"
    old_rfc_count = None
    if index_script.exists():
        existing = index_script.read_text(encoding="utf-8")
        m = re.search(r'(\d+) RFCs', existing)
        if m:
            old_rfc_count = int(m.group(1))

    # Process each RFC
    processed = []
    for md_path in md_paths:
        rfc_id = process_rfc(
            md_path, args.sprint, args.dry_run, args.md_only,
            forms_svc, drive_svc, forms_index, drive_index, pandoc_bin
        )
        processed.append(rfc_id)

    if not processed:
        print("\nNo RFCs processed.")
        return

    # Update RFC count in rebuild_rfc_index.py
    if old_rfc_count and not args.dry_run and index_script.exists():
        new_count = old_rfc_count + len(processed)
        update_rfc_count_in_script(index_script, old_rfc_count, new_count)
        print(f"\n[COUNT] Updated RFC count: {old_rfc_count} → {new_count}")

    # Regenerate RFC index README
    if not args.dry_run:
        print("\nRegenerating RFC index...")
        flag = "--md-only" if args.md_only else ""
        cmd = [sys.executable, str(index_script)]
        if flag:
            cmd.append(flag)
        subprocess.run(cmd, check=False)

    # Copy to repo and push
    if not args.md_only and not args.dry_run and REPO_DIR.exists():
        print("\nCopying files to repo/...")
        robocopy_to_repo(WORK_DIR / "02 RFCs", REPO_DIR / "02 RFCs")
        robocopy_to_repo(WORK_DIR / "scripts", REPO_DIR / "scripts", "*.py")
        robocopy_to_repo(WORK_DIR / "docs", REPO_DIR / "docs")

        message = "Add RFC(s): " + ", ".join(processed)
        git_commit_and_push(REPO_DIR, message, args.dry_run)

        # Drive sync
        print("\nSyncing to Google Drive...")
        sync_script = SCRIPT_DIR / "sync_to_gdrive.py"
        if sync_script.exists():
            subprocess.run([sys.executable, str(sync_script)], check=False)

    print(f"\n{'='*60}")
    print(f"Done. Processed: {', '.join(processed)}")
    if args.dry_run or args.md_only:
        print("Next: run without --dry-run / --md-only to push to Drive and GitHub.")


if __name__ == "__main__":
    sys.exit(main())
