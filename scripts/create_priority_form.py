"""
create_priority_form.py
-----------------------
Creates a single overall IFC5 RFC Priority Survey Google Form with:
  1. Email collection (verified)
  2. Overall comments text field
  3. One rating grid — all 38 RFCs as rows, columns: __, _, 0, 1
     (Strongly Agree / Agree / Neutral / Disagree with including/prioritising this RFC)

Saves the form to the Drive 'forms/' subfolder and records the URL in
priority_form.json alongside forms_index.json.

Usage:
    python create_priority_form.py
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
OAUTH_FILE  = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE  = SCRIPT_DIR / "oauth_token.json"
OUTPUT_FILE = SCRIPT_DIR / "priority_form.json"

DRIVE_ROOT_FOLDER = "1U9J-6hAr5pM_Q28JChDcistHsAHgi33y"
FORMS_FOLDER_NAME = "forms"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/forms.body",
]

RFCS = [
    ("IFC5-001", "Strategic Architecture Mode"),
    ("IFC5-002", "Normative Information Model Formalism"),
    ("IFC5-003", "Identity Model"),
    ("IFC5-004", "Path Model and Addressing"),
    ("IFC5-005", "Namespace and Qualified Names"),
    ("IFC5-006", "Serialization and Encoding"),
    ("IFC5-007", "Scene Graph vs. ECS vs. Hybrid Architecture"),
    ("IFC5-008", "Relationship Modeling Strategy"),
    ("IFC5-009", "Class and Type Representation"),
    ("IFC5-010", "Composition, Inheritance, and Instancing"),
    ("IFC5-011", "Document-Level Structure"),
    ("IFC5-012", "Modular Schema Imports"),
    ("IFC5-013", "Property Sets and Properties"),
    ("IFC5-014", "Geometry Architecture"),
    ("IFC5-015", "OpenUSD Alignment"),
    ("IFC5-016", "Spatial Structure"),
    ("IFC5-017", "Material Modeling"),
    ("IFC5-018", "Backward Compatibility"),
    ("IFC5-019", "Validation Framework"),
    ("IFC5-020", "Model Views and Exchange Requirements"),
    ("IFC5-021", "Federation and External References"),
    ("IFC5-022", "Versioning and Schema Evolution"),
    ("IFC5-023", "Attribute Representation"),
    ("IFC5-024", "Type System and Primitives"),
    ("IFC5-025", "Collections and Cardinality"),
    ("IFC5-026", "Openings, Voids, and Fillings"),
    ("IFC5-027", "Classification and External Dictionaries"),
    ("IFC5-028", "Units and Measures"),
    ("IFC5-029", "Presentation and Appearance"),
    ("IFC5-030", "Space Boundaries and Topology"),
    ("IFC5-031", "Metadata and Custom Data"),
    ("IFC5-032", "Extensibility"),
    ("IFC5-033", "Change, Transactions, and Collaboration"),
    ("IFC5-034", "Performance, Scale, and Database Implications"),
    ("IFC5-035", "Web and Linked-Data Alignment"),
    ("IFC5-036", "AI and Machine-Readability"),
    ("IFC5-037", "Security and Trust"),
    ("IFC5-038", "Governance, Conformance, and Interoperability Testing"),
]


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


def get_or_create_forms_folder(drive_svc):
    q = (
        f"name='{FORMS_FOLDER_NAME}' and mimeType='application/vnd.google-apps.folder'"
        f" and '{DRIVE_ROOT_FOLDER}' in parents and trashed=false"
    )
    results = drive_svc.files().list(q=q, fields="files(id)").execute()
    files = results.get("files", [])
    if files:
        return files[0]["id"]
    meta = {
        "name": FORMS_FOLDER_NAME,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [DRIVE_ROOT_FOLDER],
    }
    folder = drive_svc.files().create(body=meta, fields="id").execute()
    print(f"  [FOLDER] Created '{FORMS_FOLDER_NAME}'")
    return folder["id"]


def move_to_folder(drive_svc, file_id, folder_id):
    file_meta = drive_svc.files().get(fileId=file_id, fields="parents").execute()
    old_parents = ",".join(file_meta.get("parents", []))
    drive_svc.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=old_parents,
        fields="id,parents",
    ).execute()


def main():
    if OUTPUT_FILE.exists():
        existing = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        print(f"Priority form already exists: {existing.get('url')}")
        print("Delete priority_form.json to recreate.")
        return

    print("Authenticating...")
    forms_svc, drive_svc = get_services()

    print("Creating form...")
    form = forms_svc.forms().create(body={
        "info": {"title": "IFC5 RFC Priority Survey"}
    }).execute()
    form_id = form["formId"]
    print(f"  Form ID: {form_id}")

    # Enable email collection + set description
    forms_svc.forms().batchUpdate(formId=form_id, body={"requests": [
        {
            "updateSettings": {
                "settings": {"emailCollectionType": "VERIFIED"},
                "updateMask": "emailCollectionType"
            }
        },
        {
            "updateFormInfo": {
                "info": {
                    "title": "IFC5 RFC Priority Survey",
                    "description": (
                        "This survey collects your agreement with including and prioritising each of the "
                        "38 IFC5 Architecture RFCs.\n\n"
                        "For each RFC, indicate your level of agreement that this topic should be "
                        "resolved as part of the IFC5 architecture work:\n\n"
                        "  __  Strongly Agree — must be resolved\n"
                        "  _   Agree — should be resolved\n"
                        "  0   Neutral — no strong view\n"
                        "  1   Disagree — too early, out of scope, or should be deferred\n\n"
                        "Leave overall comments at the top if you have broader feedback on the process "
                        "or scope of the initiative."
                    ),
                },
                "updateMask": "title,description"
            }
        }
    ]}).execute()

    # Build items
    requests = []

    # Overall comments
    requests.append({
        "createItem": {
            "item": {
                "title": "Overall comments",
                "description": (
                    "Broader feedback on the RFC initiative, scope, process, or anything "
                    "not covered by the grid below."
                ),
                "questionItem": {
                    "question": {
                        "required": False,
                        "textQuestion": {"paragraph": True},
                    }
                },
            },
            "location": {"index": 0},
        }
    })

    # RFC rating grid — split into two grids to stay under API limits (max ~20 rows each)
    tier_groups = [
        ("Tier 1 — Foundational (RFCs 001–006)", RFCS[0:6]),
        ("Tier 2 — Core Architecture (RFCs 007–012, 023–025)", RFCS[6:12] + RFCS[22:25]),
        ("Tier 3 — Domain Modeling (RFCs 013–017, 026–031)", RFCS[12:17] + RFCS[25:31]),
        ("Tier 4 — Governance & Interop (RFCs 018–022, 032–038)", RFCS[17:22] + RFCS[31:38]),
    ]

    idx = 1
    for group_title, group_rfcs in tier_groups:
        row_questions = [
            {"rowQuestion": {"title": f"{rfc_id} — {title}"}}
            for rfc_id, title in group_rfcs
        ]
        requests.append({
            "createItem": {
                "item": {
                    "title": group_title,
                    "questionGroupItem": {
                        "questions": row_questions,
                        "grid": {
                            "columns": {
                                "type": "RADIO",
                                "options": [
                                    {"value": "__"},
                                    {"value": "_"},
                                    {"value": "0"},
                                    {"value": "1"},
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

    forms_svc.forms().batchUpdate(
        formId=form_id,
        body={"requests": requests}
    ).execute()
    print("  Items created.")

    # Move to forms/ folder on Drive
    print("Moving to Drive forms/ folder...")
    folder_id = get_or_create_forms_folder(drive_svc)
    move_to_folder(drive_svc, form_id, folder_id)

    # Get responder URL
    form_info = forms_svc.forms().get(formId=form_id).execute()
    responder_url = form_info.get("responderUri", f"https://docs.google.com/forms/d/{form_id}/viewform")
    edit_url = f"https://docs.google.com/forms/d/{form_id}/edit"

    result = {"id": form_id, "url": responder_url, "edit": edit_url}
    OUTPUT_FILE.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"\n✓ Priority form created.")
    print(f"  Responder URL: {responder_url}")
    print(f"  Edit URL:      {edit_url}")
    print(f"  Saved to:      {OUTPUT_FILE}")


if __name__ == "__main__":
    sys.exit(main())
