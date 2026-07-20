"""
update_priority_form.py
-----------------------
Rebuilds the IFC5 RFC Priority Survey form with updated structure:
  Columns: 1, 2, 3
  1 = Top priority to solve (select no more than 3)
  2 = Next up
  3 = Backlog / low priority / has antecedents

Usage:
    python update_priority_form.py
"""

import json
import sys
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
OAUTH_FILE  = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE  = SCRIPT_DIR / "oauth_token.json"
FORM_FILE   = SCRIPT_DIR / "priority_form.json"

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
    ("IFC5-039", "Foundational JSON Data Model"),
    ("IFC5-040", "Archetypes, Type Templates, and Override Mechanisms"),
    ("IFC5-041", "Open World vs. Closed World Assumptions"),
]

TIER_GROUPS = [
    ("Tier 1 — Foundational (RFCs 001–006, 039, 041)", RFCS[0:6] + [RFCS[38]] + [RFCS[40]]),
    ("Tier 2 — Core Architecture (RFCs 007–012, 023–025, 040)", RFCS[6:12] + RFCS[22:25] + [RFCS[39]]),
    ("Tier 3 — Domain Modeling (RFCs 013–017, 026–031)", RFCS[12:17] + RFCS[25:31]),
    ("Tier 4 — Governance & Interop (RFCs 018–022, 032–038)", RFCS[17:22] + RFCS[31:38]),
]


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


def main():
    if not FORM_FILE.exists():
        print("ERROR: priority_form.json not found. Run create_priority_form.py first.")
        sys.exit(1)

    form_info = json.loads(FORM_FILE.read_text(encoding="utf-8"))
    form_id = form_info["id"]
    print(f"Updating form: {form_id}")

    svc = get_forms_service()

    # Clear existing items
    form = svc.forms().get(formId=form_id).execute()
    items = form.get("items", [])
    if items:
        print(f"  Clearing {len(items)} existing items...")
        svc.forms().batchUpdate(formId=form_id, body={"requests": [
            {"deleteItem": {"location": {"index": 0}}} for _ in items
        ]}).execute()

    # Update title and description
    svc.forms().batchUpdate(formId=form_id, body={"requests": [
        {
            "updateFormInfo": {
                "info": {
                    "title": "IFC5 RFC Priority Survey",
                    "description": (
                        "Rate the priority of each IFC5 RFC using the scale below.\n\n"
                        "  1 = Top priority to solve — select no more than 3 across the whole list\n"
                        "  2 = Next up — important but not urgent\n"
                        "  3 = Backlog / low priority / has antecedents that must resolve first\n\n"
                        "Leave cells blank if you have no view on an RFC. "
                        "Add broader comments in the field at the top."
                    ),
                },
                "updateMask": "title,description"
            }
        }
    ]}).execute()

    # Build items
    requests = []

    # Overall comments (index 0)
    requests.append({
        "createItem": {
            "item": {
                "title": "Overall comments",
                "description": "Broader feedback on scope, process, missing topics, or anything not covered by the grid.",
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

    # One grid per tier
    for idx, (group_title, group_rfcs) in enumerate(TIER_GROUPS, start=1):
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
                                    {"value": "1"},
                                    {"value": "2"},
                                    {"value": "3"},
                                ]
                            },
                            "shuffleQuestions": False,
                        }
                    },
                },
                "location": {"index": idx},
            }
        })

    print(f"  Creating {len(requests)} items...")
    svc.forms().batchUpdate(formId=form_id, body={"requests": requests}).execute()

    print(f"\n✓ Done.")
    print(f"  Responder URL: {form_info['url']}")
    print(f"  Edit URL:      {form_info['edit']}")


if __name__ == "__main__":
    sys.exit(main())
