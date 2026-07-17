"""
create_rfc_forms.py
-------------------
Creates one Google Form per RFC, pre-populated with the RFC's Open Questions
and a general comments field. Stores form URLs in forms_index.json.

Also updates each RFC .md file with a link to its form.

Requirements:
    pip install google-api-python-client google-auth google-auth-oauthlib --break-system-packages
    Delete oauth_token.json before first run (needs new Forms API scope).

Usage:
    python create_rfc_forms.py [--dry-run]
    python create_rfc_forms.py --update-docs   (also updates Google Docs)
"""

import argparse
import json
import re
import sys
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR      = Path(__file__).resolve().parent
WORK_DIR        = SCRIPT_DIR.parent
RFC_DIR         = WORK_DIR / "02 RFCs"
FORMS_INDEX     = SCRIPT_DIR / "forms_index.json"
DRIVE_INDEX     = SCRIPT_DIR / "drive_index.json"
OAUTH_FILE      = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE      = SCRIPT_DIR / "oauth_token.json"

ROOT_FOLDER_ID  = "1U9J-6hAr5pM_Q28JChDcistHsAHgi33y"
FORMS_FOLDER_NAME = "forms"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body",
]

SENTINEL = "<!-- rfc-form -->"

# RFC metadata: (id, slug)
RFCS = [
    ("IFC5-001", "RFC-IFC5-001-strategic-architecture-mode"),
    ("IFC5-002", "RFC-IFC5-002-normative-model-formalism"),
    ("IFC5-003", "RFC-IFC5-003-identity-model"),
    ("IFC5-004", "RFC-IFC5-004-path-model"),
    ("IFC5-005", "RFC-IFC5-005-namespaces"),
    ("IFC5-006", "RFC-IFC5-006-serialization-encoding"),
    ("IFC5-007", "RFC-IFC5-007-scene-graph-vs-ecs"),
    ("IFC5-008", "RFC-IFC5-008-relationship-modeling"),
    ("IFC5-009", "RFC-IFC5-009-class-type-representation"),
    ("IFC5-010", "RFC-IFC5-010-composition-inheritance"),
    ("IFC5-011", "RFC-IFC5-011-document-structure"),
    ("IFC5-012", "RFC-IFC5-012-modular-schema-imports"),
    ("IFC5-013", "RFC-IFC5-013-property-sets"),
    ("IFC5-014", "RFC-IFC5-014-geometry-architecture"),
    ("IFC5-015", "RFC-IFC5-015-openusd-alignment"),
    ("IFC5-016", "RFC-IFC5-016-spatial-structure"),
    ("IFC5-017", "RFC-IFC5-017-material-modeling"),
    ("IFC5-018", "RFC-IFC5-018-backward-compatibility"),
    ("IFC5-019", "RFC-IFC5-019-validation-framework"),
    ("IFC5-020", "RFC-IFC5-020-model-views-exchange"),
    ("IFC5-021", "RFC-IFC5-021-federation-external-references"),
    ("IFC5-022", "RFC-IFC5-022-versioning-schema-evolution"),
    ("IFC5-023", "RFC-IFC5-023-attribute-representation"),
    ("IFC5-024", "RFC-IFC5-024-type-system-primitives"),
    ("IFC5-025", "RFC-IFC5-025-collections-cardinality"),
    ("IFC5-026", "RFC-IFC5-026-openings-voids-fillings"),
    ("IFC5-027", "RFC-IFC5-027-classification-external-dictionaries"),
    ("IFC5-028", "RFC-IFC5-028-units-measures"),
    ("IFC5-029", "RFC-IFC5-029-presentation-appearance"),
    ("IFC5-030", "RFC-IFC5-030-space-boundaries"),
    ("IFC5-031", "RFC-IFC5-031-metadata-custom-data"),
    ("IFC5-032", "RFC-IFC5-032-extensibility"),
    ("IFC5-033", "RFC-IFC5-033-change-collaboration"),
    ("IFC5-034", "RFC-IFC5-034-performance-scale-database"),
    ("IFC5-035", "RFC-IFC5-035-web-linked-data"),
    ("IFC5-036", "RFC-IFC5-036-ai-machine-readability"),
    ("IFC5-037", "RFC-IFC5-037-security-trust"),
    ("IFC5-038", "RFC-IFC5-038-governance-conformance"),
]

# ── Auth ───────────────────────────────────────────────────────────────────────

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

    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    forms = build("forms", "v1", credentials=creds, cache_discovery=False)
    return drive, forms

# ── Drive helpers ──────────────────────────────────────────────────────────────

def get_or_create_folder(drive, name, parent_id):
    q = (
        f"name='{name}' and mimeType='application/vnd.google-apps.folder'"
        f" and '{parent_id}' in parents and trashed=false"
    )
    results = drive.files().list(q=q, fields="files(id)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    meta = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    folder = drive.files().create(body=meta, fields="id").execute()
    print(f"  [FOLDER] Created '{name}' in Drive")
    return folder["id"]

# ── Question extraction ────────────────────────────────────────────────────────

def extract_questions(md_path):
    """Extract Q1, Q2... questions from the Open Questions section of an RFC."""
    text = md_path.read_text(encoding="utf-8")

    # Find Open Questions section
    section_match = re.search(
        r'##\s+\d*\.?\s*Open Questions\s*\n(.*?)(?=\n##|\Z)',
        text, re.DOTALL | re.IGNORECASE
    )
    if not section_match:
        return []

    section = section_match.group(1)
    # Match **Q1.** or Q1. at start of line
    questions = re.findall(
        r'\*{0,2}Q(\d+)\.\*{0,2}\s+(.+?)(?=\n\*{0,2}Q\d+\.|\Z)',
        section, re.DOTALL
    )
    return [(f"Q{num}", text.strip().replace("\n", " ")) for num, text in questions]

# ── Forms API ─────────────────────────────────────────────────────────────────

def create_form(forms_service, rfc_id, title, questions, forms_folder_id, drive_service):
    """Create a Google Form for one RFC. Returns (form_id, responder_url)."""

    # Step 1: Create the bare form
    form_body = {
        "info": {
            "title": f"{rfc_id} Feedback Form",
            "documentTitle": f"{rfc_id} — {title}",
        }
    }
    form = forms_service.forms().create(body=form_body).execute()
    form_id = form["formId"]
    responder_url = form["responderUri"]

    # Step 2: Move form to forms folder in Drive
    drive_service.files().update(
        fileId=form_id,
        addParents=forms_folder_id,
        removeParents="root",
        fields="id,parents",
        supportsAllDrives=True,
    ).execute()

    # Step 3: Build batch update with all questions
    items = []

    # Description item
    items.append({
        "createItem": {
            "item": {
                "title": f"Feedback form for {rfc_id}",
                "description": (
                    f"Use this form to submit structured feedback on {rfc_id}. "
                    "You can save your progress and return later using the link "
                    "Google sends to your email after clicking 'Save and fill in later' "
                    "in the three-dot menu at the top right."
                ),
                "itemId": "desc",
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {"paragraph": False},
                    }
                },
            },
            "location": {"index": 0},
        }
    })
    # Remove the placeholder description item — actually let's just use questions directly

    # Reset items and build properly
    items = []
    idx = 0

    # Open Questions
    if questions:
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

    # General comments
    items.append({
        "createItem": {
            "item": {
                "title": "General comments on this RFC",
                "description": "Any other feedback, concerns, or support not covered by the questions above.",
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

    # Comment type classification
    items.append({
        "createItem": {
            "item": {
                "title": "Comment classification",
                "description": "Select all that apply to your feedback above.",
                "questionItem": {
                    "question": {
                        "required": False,
                        "choiceQuestion": {
                            "type": "CHECKBOX",
                            "options": [
                                {"value": "Editorial — grammar or clarity"},
                                {"value": "Technical Defect — error of fact or logic"},
                                {"value": "Semantic Concern"},
                                {"value": "Compatibility Concern — conflicts with IFC4.x"},
                                {"value": "Alternative Proposal"},
                                {"value": "Evidence — supporting data or prototypes"},
                                {"value": "Blocking Objection — RFC cannot advance as written"},
                                {"value": "General Support"},
                            ],
                        },
                    }
                },
            },
            "location": {"index": idx},
        }
    })

    if items:
        forms_service.forms().batchUpdate(
            formId=form_id,
            body={"requests": items},
        ).execute()

    return form_id, responder_url

# ── MD patching ───────────────────────────────────────────────────────────────

def patch_md(md_path, rfc_id, form_url, dry_run):
    content = md_path.read_text(encoding="utf-8")
    if SENTINEL in content:
        return "SKIP"

    form_line = (
        f"\n{SENTINEL}\n"
        f"📋 **[Take the feedback form for {rfc_id}]({form_url})**"
        f" — answer the open questions and leave comments directly.\n"
    )

    # Insert after the header blockquote (first blank line after the > block)
    # Find end of header sentinel block
    header_end = content.find("\n\n", content.find("<!-- rfc-links -->"))
    if header_end == -1:
        new_content = form_line + content
    else:
        new_content = content[:header_end] + form_line + content[header_end:]

    if not dry_run:
        md_path.write_text(new_content, encoding="utf-8")
    return "PATCH"

# ── Google Doc patching ───────────────────────────────────────────────────────

def patch_gdoc(drive_service, file_id, rfc_id, form_url):
    """Append a form link to an existing Google Doc."""
    from googleapiclient.discovery import build

    # We'll use the Docs API to append text
    docs = build("docs", "v1", credentials=drive_service._http.credentials, cache_discovery=False)

    doc = docs.documents().get(documentId=file_id).execute()
    content = doc.get("body", {}).get("content", [])
    # Find end index
    end_index = 1
    for element in content:
        if "endIndex" in element:
            end_index = element["endIndex"]

    # Check if form link already added
    full_text = ""
    for element in content:
        para = element.get("paragraph", {})
        for elem in para.get("elements", []):
            full_text += elem.get("textRun", {}).get("content", "")
    if "feedback form" in full_text.lower() and rfc_id in full_text:
        return "SKIP"

    requests = [
        {
            "insertText": {
                "location": {"index": end_index - 1},
                "text": f"\n\n📋 Feedback Form: {form_url}\nAnswer the open questions and leave comments directly.\n"
            }
        }
    ]
    docs.documents().batchUpdate(
        documentId=file_id,
        body={"requests": requests}
    ).execute()
    return "PATCH"

# ── Index helpers ─────────────────────────────────────────────────────────────

def load_json(path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}

def save_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

# ── RFC title extraction ──────────────────────────────────────────────────────

def extract_title(md_path):
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# RFC"):
            # e.g. "# RFC-IFC5-001: Strategic Architecture Mode"
            parts = line.split(":", 1)
            if len(parts) > 1:
                return parts[1].strip()
        if line.startswith("## ") and "Title" not in line and "Open" not in line:
            return line.lstrip("# ").strip()
    return md_path.stem

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update-docs", action="store_true",
                        help="Also update Google Docs with form links")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    drive_service, forms_service = get_services()
    forms_index = load_json(FORMS_INDEX)
    drive_index = load_json(DRIVE_INDEX)

    # Get or create forms/ folder in Drive
    forms_folder_id = get_or_create_folder(drive_service, FORMS_FOLDER_NAME, ROOT_FOLDER_ID)

    for rfc_id, slug in RFCS:
        md_path = RFC_DIR / f"{slug}.md"
        if not md_path.exists():
            print(f"  [WARN] Not found: {md_path.name}")
            continue

        title = extract_title(md_path)
        questions = extract_questions(md_path)
        print(f"\n{rfc_id} — {title} ({len(questions)} questions)")

        # Create or skip form
        if rfc_id in forms_index:
            form_url = forms_index[rfc_id]["url"]
            print(f"  [SKIP] Form already exists: {form_url}")
        else:
            if not args.dry_run:
                form_id, form_url = create_form(
                    forms_service, rfc_id, title, questions,
                    forms_folder_id, drive_service
                )
                forms_index[rfc_id] = {"id": form_id, "url": form_url}
                print(f"  [CREATE] {form_url}")
            else:
                form_url = "https://forms.google.com/dry-run"
                print(f"  [DRY] Would create form with {len(questions)} questions")

        # Patch .md file
        result = patch_md(md_path, rfc_id, form_url, dry_run=args.dry_run)
        print(f"  [MD {result}] {md_path.name}")

        # Patch Google Doc
        if args.update_docs:
            drive_key = f"02 RFCs\\{slug}.md"
            # Try both path separators
            file_id = drive_index.get(drive_key) or drive_index.get(drive_key.replace("\\", "/"))
            if file_id:
                if not args.dry_run:
                    r = patch_gdoc(drive_service, file_id, rfc_id, form_url)
                    print(f"  [DOC {r}]")
                else:
                    print(f"  [DRY] Would patch Google Doc {file_id}")
            else:
                print(f"  [DOC SKIP] Not in drive_index — run sync_to_gdrive.py first")

    if not args.dry_run:
        save_json(FORMS_INDEX, forms_index)
        print(f"\n✓ forms_index.json updated ({len(forms_index)} forms)")

    print("\n✓ Done.")

if __name__ == "__main__":
    sys.exit(main())
