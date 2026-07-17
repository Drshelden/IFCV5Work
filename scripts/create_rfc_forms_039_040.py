"""
create_rfc_forms_039_040.py
---------------------------
Creates Google Forms for RFC-IFC5-039 and RFC-IFC5-040 (new RFCs added after
the initial 38). Saves results to forms_index.json. Also runs rebuild_rfc_headers.py
logic to patch the nav blocks in the two new .md files.

Usage:
    python create_rfc_forms_039_040.py [--dry-run]
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
WORK_DIR    = SCRIPT_DIR.parent
RFC_DIR     = WORK_DIR / "02 RFCs"
FORMS_INDEX = SCRIPT_DIR / "forms_index.json"
DRIVE_INDEX = SCRIPT_DIR / "drive_index.json"
OAUTH_FILE  = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE  = SCRIPT_DIR / "oauth_token.json"

REPO = "https://github.com/Drshelden/IFCV5Work"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body",
]

# New RFCs: (id, slug, tier_slug)
NEW_RFCS = [
    (
        "IFC5-039",
        "RFC-IFC5-039-foundational-json-data-model",
        "-tier-1-foundational",
    ),
    (
        "IFC5-040",
        "RFC-IFC5-040-archetypes-templates-overrides",
        "-tier-2-core-architecture",
    ),
]

ENCODED_BODY = (
    "%2A%2AComment%20type%3A%2A%2A%20Editorial%20%7C%20Technical%20Defect%20%7C%20Semantic%20Concern%20%7C"
    "%20Compatibility%20Concern%20%7C%20Alternative%20Proposal%20%7C%20Evidence%20%7C%20Blocking%20Objection%20%7C%20General%20Support"
    "%0A%0A%2A%28delete%20all%20but%20one%29%2A%0A%0A---%0A%0A%2A%2AFeedback%3A%2A%2A%0A%0A"
    "%3C%21--%20Be%20specific%20%E2%80%94%20reference%20section%20numbers%20or%20quote%20RFC%20text%20where%20relevant%20--%3E"
    "%0A%0A---%0A%0A%2A%2ASupporting%20evidence%20or%20examples%3A%2A%2A%0A%0A"
    "%3C%21--%20Optional%3A%20links%2C%20code%2C%20schema%20examples%2C%20prior%20art%20--%3E"
    "%0A%0A---%0A%0A%2A%2AQuestions%20for%20the%20working%20group%3A%2A%2A%0A%0A"
    "%3C%21--%20Optional%3A%20number%20each%20question%20Q1%2C%20Q2%2C%20...%20--%3E%0A"
)


# ── Auth ──────────────────────────────────────────────────────────────────────

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

    forms_svc = build("forms", "v1", credentials=creds, cache_discovery=False)
    drive_svc = build("drive", "v3", credentials=creds, cache_discovery=False)
    return forms_svc, drive_svc


# ── RFC content extraction ─────────────────────────────────────────────────────

def extract_approaches(md_path):
    text = md_path.read_text(encoding="utf-8")
    section = re.search(
        r'##\s+\d*\.?\s*Proposed Approaches?\s*\n(.*?)(?=\n##\s|\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if not section:
        return []
    approaches = re.findall(r'###\s+[\d.]+\s+(.+)', section.group(1))
    return [a.strip() for a in approaches]


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


def extract_title(md_path):
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# RFC"):
            parts = line.split(":", 1)
            if len(parts) > 1:
                return parts[1].strip()
    return md_path.stem


# ── Form creation ─────────────────────────────────────────────────────────────

def create_form(forms_svc, drive_svc, rfc_id, title, approaches, questions,
                forms_folder_id, dry_run):
    """Create a new Google Form in the forms/ folder."""
    if dry_run:
        print(f"  [DRY] Would create form: {rfc_id} — {title}")
        print(f"        {len(approaches)} approaches, {len(questions)} questions")
        return None

    # Create blank form
    form = forms_svc.forms().create(
        body={"info": {"title": f"{rfc_id} Feedback Form"}}
    ).execute()
    form_id = form["formId"]
    responder_url = form["responderUri"]

    # Move to forms/ folder (Drive API)
    file_meta = drive_svc.files().get(
        fileId=form_id, fields="parents", supportsAllDrives=True
    ).execute()
    old_parents = ",".join(file_meta.get("parents", []))
    drive_svc.files().update(
        fileId=form_id,
        addParents=forms_folder_id,
        removeParents=old_parents,
        supportsAllDrives=True,
    ).execute()

    # Build full GitHub URL for new discussion link
    new_disc_url = (
        f"{REPO}/discussions/new"
        f"?category=-tier-1-foundational"  # placeholder, overridden per RFC below
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}"
        f"&body={ENCODED_BODY}"
    )
    github_url  = f"{REPO}/blob/master/02%20RFCs/{rfc_id.lower().replace('-','')}.md"
    view_url    = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"

    links_text = (
        f"📄 GitHub MD: {REPO}/blob/master/02%20RFCs/RFC-{rfc_id}-*.md\n"
        f"💬 View all discussions: {view_url}\n"
        f"+ New discussion: {new_disc_url}\n"
        f"📋 Take this feedback form: {responder_url}"
    )

    # Enable email collection + set description
    requests = [
        {
            "updateSettings": {
                "settings": {"emailCollectionType": "VERIFIED"},
                "updateMask": "emailCollectionType"
            }
        },
        {
            "updateFormInfo": {
                "info": {
                    "title": f"{rfc_id} Feedback Form",
                    "description": (
                        f"Structured feedback form for {rfc_id} — {title}. "
                        "Your email is collected so you can receive a copy of your responses "
                        "and return to edit them."
                    ),
                },
                "updateMask": "title,description"
            }
        },
    ]

    # Items
    idx = 0
    items = []

    # General comments
    items.append({
        "createItem": {
            "item": {
                "title": "General comments on this RFC",
                "description": "Overall feedback, concerns, or support. Leave blank if you have none.",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {"paragraph": True},
                    }
                },
            },
            "location": {"index": idx},
        }
    })
    idx += 1

    # Rating grid
    if approaches:
        row_questions = [{"rowQuestion": {"title": a}} for a in approaches]
        items.append({
            "createItem": {
                "item": {
                    "title": "Rate each proposed approach",
                    "description": (
                        "++ = strongly support  |  + = support  |  "
                        "0 = no strong view (default)  |  - = oppose"
                    ),
                    "questionGroupItem": {
                        "questions": row_questions,
                        "grid": {
                            "columns": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "++"},
                                    {"value": "+"},
                                    {"value": "0"},
                                    {"value": "-"},
                                ]
                            },
                            "shuffleQuestions": False,
                        }
                    },
                },
                "location": {"index": idx},
            }
        })
        idx += 1

    # Individual questions
    for q_label, q_text in questions:
        items.append({
            "createItem": {
                "item": {
                    "title": f"{q_label}. {q_text}",
                    "questionItem": {
                        "question": {
                            "required": False,
                            "textQuestion": {"paragraph": True},
                        }
                    },
                },
                "location": {"index": idx},
            }
        })
        idx += 1

    # Links section
    items.append({
        "createItem": {
            "item": {
                "title": "Links for this RFC",
                "description": links_text,
                "textItem": {},
            },
            "location": {"index": idx},
        }
    })

    forms_svc.forms().batchUpdate(
        formId=form_id,
        body={"requests": requests + items}
    ).execute()

    return {
        "id": form_id,
        "url": responder_url,
        "edit": f"https://docs.google.com/forms/d/{form_id}/edit",
    }


# ── Patch .md nav block ────────────────────────────────────────────────────────

def patch_md_nav(md_path, rfc_id, slug, tier_slug, form_url, gdoc_url):
    """Replace PENDING placeholders in the rfc-nav and rfc-form blocks."""
    text = md_path.read_text(encoding="utf-8")

    gh_url   = f"{REPO}/blob/master/02%20RFCs/{slug}.md"
    view_url = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"
    new_url  = (
        f"{REPO}/discussions/new"
        f"?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}"
        f"&body={ENCODED_BODY}"
    )
    doc_part = f"[📝 Google Doc]({gdoc_url}) · " if gdoc_url else ""

    nav_line = (
        f"[📄 GitHub MD]({gh_url}) · "
        f"{doc_part}"
        f"[💬 View all discussions]({view_url}) · "
        f"[+ New discussion]({new_url}) · "
        f"[📋 Take the feedback form]({form_url})"
    )
    form_line = (
        f'📋 **[Take the feedback form for {rfc_id}]({form_url})** '
        f'— answer the open questions and leave comments directly.'
    )

    # Replace PENDING in rfc-form line
    text = re.sub(
        r'(<!-- rfc-form -->\n).*?(\n<!-- rfc-nav -->)',
        lambda m: m.group(1) + form_line + m.group(2),
        text, flags=re.DOTALL
    )
    # Replace PENDING in rfc-nav lines (both header and footer)
    text = re.sub(
        r'(<!-- rfc-nav -->\n)[^\n]+',
        lambda m: m.group(1) + nav_line,
        text
    )

    md_path.write_text(text, encoding="utf-8")
    print(f"  [MD PATCH] {md_path.name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    # Load existing indexes
    forms_index = json.loads(FORMS_INDEX.read_text(encoding="utf-8")) if FORMS_INDEX.exists() else {}
    drive_index = json.loads(DRIVE_INDEX.read_text(encoding="utf-8")) if DRIVE_INDEX.exists() else {}

    # Find forms folder ID from drive_index (look for any forms/ path entry, or use the known parent)
    # The forms/ folder is under ROOT_FOLDER_ID — look it up or hard-code from create_priority_form.py context
    # We'll find it by looking at an existing form's parent via Drive API
    FORMS_FOLDER_ID = "REPLACE_WITH_FORMS_FOLDER_ID"  # Set this before running!

    if not args.dry_run:
        forms_svc, drive_svc = get_services()

        # Auto-detect forms folder from an existing form if possible
        if forms_index:
            sample_form_id = next(iter(forms_index.values()), {}).get("id")
            if sample_form_id:
                try:
                    meta = drive_svc.files().get(
                        fileId=sample_form_id, fields="parents", supportsAllDrives=True
                    ).execute()
                    parents = meta.get("parents", [])
                    if parents:
                        FORMS_FOLDER_ID = parents[0]
                        print(f"Auto-detected forms folder: {FORMS_FOLDER_ID}")
                except Exception as e:
                    print(f"WARNING: Could not auto-detect forms folder: {e}")
    else:
        forms_svc = drive_svc = None

    for rfc_id, slug, tier_slug in NEW_RFCS:
        md_path = RFC_DIR / f"{slug}.md"
        if not md_path.exists():
            print(f"ERROR: {md_path} not found. Create the .md file first.")
            continue

        print(f"\n--- {rfc_id} ---")

        if rfc_id in forms_index:
            print(f"  [SKIP] Form already exists: {forms_index[rfc_id]['url']}")
        else:
            title     = extract_title(md_path)
            approaches = extract_approaches(md_path)
            questions  = extract_questions(md_path)
            print(f"  Title:     {title}")
            print(f"  Approaches: {approaches}")
            print(f"  Questions:  {[q[0] for q in questions]}")

            result = create_form(
                forms_svc, drive_svc, rfc_id, title, approaches, questions,
                FORMS_FOLDER_ID, args.dry_run
            )
            if result:
                forms_index[rfc_id] = result
                FORMS_INDEX.write_text(json.dumps(forms_index, indent=2), encoding="utf-8")
                print(f"  [CREATE] {result['url']}")

        # Patch .md nav block
        if rfc_id in forms_index and not args.dry_run:
            form_url = forms_index[rfc_id]["url"]
            drive_key = f"02 RFCs\\{slug}.md"
            doc_id = drive_index.get(drive_key) or drive_index.get(drive_key.replace("\\", "/"))
            gdoc_url = f"https://docs.google.com/document/d/{doc_id}/edit" if doc_id else None
            patch_md_nav(md_path, rfc_id, slug, tier_slug, form_url, gdoc_url)
        elif args.dry_run:
            print(f"  [DRY] Would patch nav block in {slug}.md")

    print("\n=== Done ===")
    print("Next steps:")
    print("  1. Run sync_to_gdrive.py to upload the new .md files as Google Docs")
    print("  2. Run create_rfc_forms_039_040.py again (it will now find Drive doc IDs and patch navs)")
    print("  3. Run update_priority_form.py to add IFC5-039 and IFC5-040 to the priority survey")
    print("  4. Run sync_and_push.bat to push everything to GitHub")


if __name__ == "__main__":
    sys.exit(main())
