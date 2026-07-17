"""
update_rfc_forms.py
-------------------
Updates all existing RFC Google Forms with the revised structure:
  1. Email collection enabled (verified)
  2. General comments (top)
  3. Rating grid: one row per proposed approach, columns: ++, +, 0, -
  4. Individual Q1, Q2... questions
  (comment classification removed)

Requires forms_index.json from create_rfc_forms.py.

Usage:
    python update_rfc_forms.py [--dry-run]
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
WORK_DIR     = SCRIPT_DIR.parent
RFC_DIR      = WORK_DIR / "02 RFCs"
FORMS_INDEX  = SCRIPT_DIR / "forms_index.json"
DRIVE_INDEX  = SCRIPT_DIR / "drive_index.json"
OAUTH_FILE   = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE   = SCRIPT_DIR / "oauth_token.json"

REPO = "https://github.com/Drshelden/IFCV5Work"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body",
]

RFCS = [
    ("IFC5-001","RFC-IFC5-001-strategic-architecture-mode",        "-tier-1-foundational"),
    ("IFC5-002","RFC-IFC5-002-normative-model-formalism",          "-tier-1-foundational"),
    ("IFC5-003","RFC-IFC5-003-identity-model",                     "-tier-1-foundational"),
    ("IFC5-004","RFC-IFC5-004-path-model",                         "-tier-1-foundational"),
    ("IFC5-005","RFC-IFC5-005-namespaces",                         "-tier-1-foundational"),
    ("IFC5-006","RFC-IFC5-006-serialization-encoding",             "-tier-1-foundational"),
    ("IFC5-007","RFC-IFC5-007-scene-graph-vs-ecs",                 "-tier-2-core-architecture"),
    ("IFC5-008","RFC-IFC5-008-relationship-modeling",              "-tier-2-core-architecture"),
    ("IFC5-009","RFC-IFC5-009-class-type-representation",          "-tier-2-core-architecture"),
    ("IFC5-010","RFC-IFC5-010-composition-inheritance",            "-tier-2-core-architecture"),
    ("IFC5-011","RFC-IFC5-011-document-structure",                 "-tier-2-core-architecture"),
    ("IFC5-012","RFC-IFC5-012-modular-schema-imports",             "-tier-2-core-architecture"),
    ("IFC5-013","RFC-IFC5-013-property-sets",                      "-tier-3-domain-modeling"),
    ("IFC5-014","RFC-IFC5-014-geometry-architecture",              "-tier-3-domain-modeling"),
    ("IFC5-015","RFC-IFC5-015-openusd-alignment",                  "-tier-3-domain-modeling"),
    ("IFC5-016","RFC-IFC5-016-spatial-structure",                  "-tier-3-domain-modeling"),
    ("IFC5-017","RFC-IFC5-017-material-modeling",                  "-tier-3-domain-modeling"),
    ("IFC5-018","RFC-IFC5-018-backward-compatibility",             "-tier-4-governance"),
    ("IFC5-019","RFC-IFC5-019-validation-framework",               "-tier-4-governance"),
    ("IFC5-020","RFC-IFC5-020-model-views-exchange",               "-tier-4-governance"),
    ("IFC5-021","RFC-IFC5-021-federation-external-references",     "-tier-4-governance"),
    ("IFC5-022","RFC-IFC5-022-versioning-schema-evolution",        "-tier-4-governance"),
    ("IFC5-023","RFC-IFC5-023-attribute-representation",           "-tier-2-core-architecture"),
    ("IFC5-024","RFC-IFC5-024-type-system-primitives",             "-tier-2-core-architecture"),
    ("IFC5-025","RFC-IFC5-025-collections-cardinality",            "-tier-2-core-architecture"),
    ("IFC5-026","RFC-IFC5-026-openings-voids-fillings",            "-tier-3-domain-modeling"),
    ("IFC5-027","RFC-IFC5-027-classification-external-dictionaries","-tier-3-domain-modeling"),
    ("IFC5-028","RFC-IFC5-028-units-measures",                     "-tier-3-domain-modeling"),
    ("IFC5-029","RFC-IFC5-029-presentation-appearance",            "-tier-3-domain-modeling"),
    ("IFC5-030","RFC-IFC5-030-space-boundaries",                   "-tier-3-domain-modeling"),
    ("IFC5-031","RFC-IFC5-031-metadata-custom-data",               "-tier-3-domain-modeling"),
    ("IFC5-032","RFC-IFC5-032-extensibility",                      "-tier-4-governance"),
    ("IFC5-033","RFC-IFC5-033-change-collaboration",               "-tier-4-governance"),
    ("IFC5-034","RFC-IFC5-034-performance-scale-database",         "-tier-4-governance"),
    ("IFC5-035","RFC-IFC5-035-web-linked-data",                    "-tier-4-governance"),
    ("IFC5-036","RFC-IFC5-036-ai-machine-readability",             "-tier-4-governance"),
    ("IFC5-037","RFC-IFC5-037-security-trust",                     "-tier-4-governance"),
    ("IFC5-038","RFC-IFC5-038-governance-conformance",             "-tier-4-governance"),
    ("IFC5-039","RFC-IFC5-039-foundational-json-data-model",       "-tier-1-foundational"),
    ("IFC5-040","RFC-IFC5-040-archetypes-templates-overrides",     "-tier-2-core-architecture"),
]

# ── Auth ───────────────────────────────────────────────────────────────────────

def get_forms_service():
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

    return build("forms", "v1", credentials=creds, cache_discovery=False)

# ── RFC content extraction ─────────────────────────────────────────────────────

def extract_approaches(md_path):
    """Extract proposed approach titles from ## 4. Proposed Approaches section."""
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
    """Extract Q1, Q2... from Open Questions section."""
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

# ── Form rebuild ──────────────────────────────────────────────────────────────

def clear_form_items(forms_service, form_id):
    """Delete all existing items from a form."""
    form = forms_service.forms().get(formId=form_id).execute()
    items = form.get("items", [])
    if not items:
        return
    requests = [
        {"deleteItem": {"location": {"index": 0}}}
        for _ in items
    ]
    forms_service.forms().batchUpdate(
        formId=form_id,
        body={"requests": requests}
    ).execute()


def rebuild_form(forms_service, form_id, rfc_id, title, approaches, questions, links, dry_run):
    """Clear and rebuild a form with the new structure."""
    if dry_run:
        print(f"  [DRY] Would rebuild: {len(approaches)} approaches, {len(questions)} questions")
        return

    github_url, gdoc_url, list_url, new_url, form_url = links

    # 1. Clear existing items
    clear_form_items(forms_service, form_id)

    # 2. Enable email collection + update title
    forms_service.forms().batchUpdate(
        formId=form_id,
        body={
            "requests": [
                {
                    "updateSettings": {
                        "settings": {
                            "emailCollectionType": "VERIFIED"
                        },
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
                                "and return to edit them. "
                                "Use the three-dot menu → 'Save and fill in later' to resume later."
                            ),
                        },
                        "updateMask": "title,description"
                    }
                }
            ]
        }
    ).execute()

    # 3. Build new items
    requests = []
    idx = 0

    # General comments (top)
    requests.append({
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

    # Rating grid for proposed approaches
    if approaches:
        row_questions = [{"rowQuestion": {"title": a}} for a in approaches]
        requests.append({
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
        requests.append({
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

    # Links section (last item)
    links_text = (
        f"📄 GitHub MD: {github_url}\n"
        f"📝 Google Doc: {gdoc_url}\n"
        f"💬 View all discussions: {list_url}\n"
        f"+ New discussion: {new_url}\n"
        f"📋 Take this feedback form: {form_url}"
    )
    requests.append({
        "createItem": {
            "item": {
                "title": "Links for this RFC",
                "description": links_text,
                "textItem": {},
            },
            "location": {"index": idx},
        }
    })

    if requests:
        forms_service.forms().batchUpdate(
            formId=form_id,
            body={"requests": requests}
        ).execute()

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    if not FORMS_INDEX.exists():
        print("ERROR: forms_index.json not found. Run create_rfc_forms.py first.")
        sys.exit(1)

    forms_index = json.loads(FORMS_INDEX.read_text(encoding="utf-8"))
    drive_index = json.loads(DRIVE_INDEX.read_text(encoding="utf-8")) if DRIVE_INDEX.exists() else {}
    forms_service = get_forms_service()

    for rfc_id, slug, tier_slug in RFCS:
        md_path = RFC_DIR / f"{slug}.md"
        if not md_path.exists():
            print(f"  [WARN] {rfc_id}: MD file not found")
            continue

        if rfc_id not in forms_index:
            print(f"  [SKIP] {rfc_id}: not in forms_index — run create_rfc_forms.py first")
            continue

        form_id    = forms_index[rfc_id]["id"]
        form_url   = forms_index[rfc_id].get("url", "#")
        title      = extract_title(md_path)
        approaches = extract_approaches(md_path)
        questions  = extract_questions(md_path)

        drive_key = f"02 RFCs\\{slug}.md"
        doc_id    = drive_index.get(drive_key) or drive_index.get(drive_key.replace("\\", "/"))
        gdoc_url  = f"https://docs.google.com/document/d/{doc_id}/edit" if doc_id else "#"

        github_url = f"{REPO}/blob/master/02%20RFCs/{slug}.md"
        list_url   = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"
        new_url    = (
            f"{REPO}/discussions/new"
            f"?category={tier_slug}"
            f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
            f"&labels={rfc_id}"
        )
        links = (github_url, gdoc_url, list_url, new_url, form_url)

        print(f"{rfc_id} — {title}")
        print(f"  approaches={len(approaches)}, questions={len(questions)}")

        try:
            rebuild_form(forms_service, form_id, rfc_id, title, approaches, questions, links, args.dry_run)
            print(f"  [OK]")
        except Exception as e:
            print(f"  [ERROR] {e}")

    print("\n✓ Done.")

if __name__ == "__main__":
    sys.exit(main())
