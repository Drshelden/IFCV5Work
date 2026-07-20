"""
rebuild_rfc_index.py
--------------------
Generates 03 RFCs/README.md (GitHub version) and uploads an equivalent
Google Doc (Drive version) for the RFC Index.

Each RFC entry includes:
  - ID, Title, Prototype Required flag
  - GitHub MD link, Google Doc link
  - View discussions, + New discussion, Feedback form

Usage:
    python rebuild_rfc_index.py [--md-only]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

SCRIPT_DIR   = Path(__file__).resolve().parent
WORK_DIR     = SCRIPT_DIR.parent
RFC_DIR      = WORK_DIR / "03 RFCs"
FORMS_INDEX  = SCRIPT_DIR / "forms_index.json"
DRIVE_INDEX  = SCRIPT_DIR / "drive_index.json"
OAUTH_FILE   = SCRIPT_DIR / "oauth_client_secret.json"
TOKEN_FILE   = SCRIPT_DIR / "oauth_token.json"

REPO           = "https://github.com/Drshelden/IFCV5Work"
DRIVE_RFC_DOC  = "1L4wD92OdDVGm5cvcPiAGYWQBF9pDHbHXni6ohOS5rKE"
SCOPES         = ["https://www.googleapis.com/auth/drive"]
GDOC_MIME      = "application/vnd.google-apps.document"
DOCX_MIME      = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

BODY_TEMPLATE = (
    "**Comment type:** Editorial | Technical Defect | Semantic Concern | "
    "Compatibility Concern | Alternative Proposal | Evidence | "
    "Blocking Objection | General Support\n\n*(delete all but one)*\n\n---\n\n"
    "**Feedback:**\n\n---\n\n**Supporting evidence or examples:**\n\n---\n\n"
    "**Questions for the working group:**\n"
)
ENCODED_BODY = urllib.parse.quote(BODY_TEMPLATE, safe="")

TIERS = [
    {
        "label": "Tier 1 — Foundational",
        "note": "Resolve these before anything else. All downstream RFCs depend on them.",
        "slug": "-tier-1-foundational",
        "rfcs": [
            ("IFC5-001","RFC-IFC5-001-strategic-architecture-mode",         "Strategic Architecture Mode",                        False),
            ("IFC5-002","RFC-IFC5-002-normative-model-formalism",           "Normative Information Model Formalism",               False),
            ("IFC5-003","RFC-IFC5-003-identity-model",                      "Identity Model",                                     True),
            ("IFC5-004","RFC-IFC5-004-path-model",                          "Path Model and Addressing",                          True),
            ("IFC5-005","RFC-IFC5-005-namespaces",                          "Namespace and Qualified Names",                      False),
            ("IFC5-006","RFC-IFC5-006-serialization-encoding",              "Serialization and Encoding",                         False),
            ("IFC5-039","RFC-IFC5-039-foundational-json-data-model",        "Foundational JSON Data Model",                       False),
            ("IFC5-041","RFC-IFC5-041-open-world-vs-closed-world",         "Open World vs. Closed World Assumptions",             False),
        ],
    },
    {
        "label": "Tier 2 — Core Architecture",
        "note": "Major structural decisions. Depend on Tier 1.",
        "slug": "-tier-2-core-architecture",
        "rfcs": [
            ("IFC5-007","RFC-IFC5-007-scene-graph-vs-ecs",                  "Scene Graph vs. ECS vs. Hybrid Architecture",        True),
            ("IFC5-008","RFC-IFC5-008-relationship-modeling",               "Relationship Modeling Strategy",                     True),
            ("IFC5-009","RFC-IFC5-009-class-type-representation",           "Class and Type Representation",                      False),
            ("IFC5-010","RFC-IFC5-010-composition-inheritance",             "Composition, Inheritance, and Instancing",           True),
            ("IFC5-011","RFC-IFC5-011-document-structure",                  "Document-Level Structure",                           False),
            ("IFC5-012","RFC-IFC5-012-modular-schema-imports",              "Modular Schema Imports",                             False),
            ("IFC5-023","RFC-IFC5-023-attribute-representation",            "Attribute Representation",                           False),
            ("IFC5-024","RFC-IFC5-024-type-system-primitives",              "Type System, Primitives, Enumerations, SELECTs",     False),
            ("IFC5-025","RFC-IFC5-025-collections-cardinality",             "Collections and Cardinality",                        False),
            ("IFC5-040","RFC-IFC5-040-archetypes-templates-overrides",      "Archetypes, Type Templates, and Override Mechanisms",True),
        ],
    },
    {
        "label": "Tier 3 — Domain Modeling",
        "note": "Domain-specific decisions. Depend on Tier 2.",
        "slug": "-tier-3-domain-modeling",
        "rfcs": [
            ("IFC5-013","RFC-IFC5-013-property-sets",                       "Property Sets and Properties",                       True),
            ("IFC5-014","RFC-IFC5-014-geometry-architecture",               "Geometry Architecture",                              True),
            ("IFC5-015","RFC-IFC5-015-openusd-alignment",                   "OpenUSD Alignment",                                  True),
            ("IFC5-016","RFC-IFC5-016-spatial-structure",                   "Spatial Structure and Decomposition",                False),
            ("IFC5-017","RFC-IFC5-017-material-modeling",                   "Material Modeling",                                  False),
            ("IFC5-026","RFC-IFC5-026-openings-voids-fillings",             "Openings, Voids, and Fillings",                      True),
            ("IFC5-027","RFC-IFC5-027-classification-external-dictionaries","Classification and External Dictionaries",           False),
            ("IFC5-028","RFC-IFC5-028-units-measures",                      "Units and Measures",                                 False),
            ("IFC5-029","RFC-IFC5-029-presentation-appearance",             "Presentation and Appearance",                        False),
            ("IFC5-030","RFC-IFC5-030-space-boundaries",                    "Space Boundaries and Topology",                      False),
            ("IFC5-031","RFC-IFC5-031-metadata-custom-data",                "Metadata and Custom Data",                           False),
        ],
    },
    {
        "label": "Tier 4 — Process & Governance",
        "note": "Conformance, versioning, federation, and cross-cutting concerns.",
        "slug": "-tier-4-governance",
        "rfcs": [
            ("IFC5-018","RFC-IFC5-018-backward-compatibility",              "Backward Compatibility and Round-Tripping",          True),
            ("IFC5-019","RFC-IFC5-019-validation-framework",                "Validation Framework",                               False),
            ("IFC5-020","RFC-IFC5-020-model-views-exchange",                "Model Views and Exchange Requirements",              False),
            ("IFC5-021","RFC-IFC5-021-federation-external-references",      "Federation and External References",                 False),
            ("IFC5-022","RFC-IFC5-022-versioning-schema-evolution",         "Versioning and Schema Evolution",                    False),
            ("IFC5-032","RFC-IFC5-032-extensibility",                       "Extensibility",                                      False),
            ("IFC5-033","RFC-IFC5-033-change-collaboration",                "Change, Transactions, and Collaboration",            False),
            ("IFC5-034","RFC-IFC5-034-performance-scale-database",          "Performance, Scale, and Database Implications",      True),
            ("IFC5-035","RFC-IFC5-035-web-linked-data",                     "Web and Linked-Data Alignment",                      False),
            ("IFC5-036","RFC-IFC5-036-ai-machine-readability",              "AI and Machine-Readability",                         False),
            ("IFC5-037","RFC-IFC5-037-security-trust",                      "Security and Trust",                                 False),
            ("IFC5-038","RFC-IFC5-038-governance-conformance",              "Governance, Conformance, and Interoperability Testing", False),
        ],
    },
]


def load_indexes():
    forms = json.loads(FORMS_INDEX.read_text(encoding="utf-8")) if FORMS_INDEX.exists() else {}
    drive = json.loads(DRIVE_INDEX.read_text(encoding="utf-8")) if DRIVE_INDEX.exists() else {}
    return forms, drive


def rfc_urls(rfc_id, slug, tier_slug, forms_idx, drive_idx):
    gh_url   = f"{REPO}/blob/master/02%20RFCs/{slug}.md"
    view_url = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"
    new_url  = (
        f"{REPO}/discussions/new"
        f"?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}"
        f"&body={ENCODED_BODY}"
    )
    dk       = f"03 RFCs\\{slug}.md"
    doc_id   = drive_idx.get(dk) or drive_idx.get(dk.replace("\\", "/"))
    gdoc_url = f"https://docs.google.com/document/d/{doc_id}/edit" if doc_id else None
    form_url = forms_idx.get(rfc_id, {}).get("url")
    return gh_url, gdoc_url, view_url, new_url, form_url


def build_github_md(forms_idx, drive_idx):
    lines = [
        "# RFC Index",
        "",
        "**📄 GitHub (this document)** · [📝 Google Doc](https://docs.google.com/document/d/1L4wD92OdDVGm5cvcPiAGYWQBF9pDHbHXni6ohOS5rKE/edit)",
        "",
        "41 RFCs covering the major architectural decisions for IFC5. All are at **Idea** status — no decisions have been made yet. The [Decision Register](../01%20Decision%20Register/IFC5_Decision_Register.csv) is the authoritative status tracker. ⚗️ = prototype required before Committee Review.",
        "",
        "---",
        "",
    ]

    for tier in TIERS:
        lines.append(f"## {tier['label']}")
        lines.append(f"*{tier['note']}*")
        lines.append("")
        lines.append("| ID | Title | ⚗️ | GitHub · Drive | Discussions · Form |")
        lines.append("|---|---|:---:|---|---|")

        for rfc_id, slug, title, proto in tier["rfcs"]:
            gh_url, gdoc_url, view_url, new_url, form_url = rfc_urls(rfc_id, slug, tier["slug"], forms_idx, drive_idx)
            proto_cell = "⚗️" if proto else ""
            doc_cell   = f"[📄 MD]({gh_url})"
            if gdoc_url:
                doc_cell += f" · [📝 Doc]({gdoc_url})"
            disc_cell  = f"[💬 view]({view_url}) · [+ new]({new_url})"
            if form_url:
                disc_cell += f" · [📋 form]({form_url})"
            lines.append(f"| **{rfc_id}** | {title} | {proto_cell} | {doc_cell} | {disc_cell} |")

        lines.append("")

    lines += [
        "---",
        "",
        "*[📋 RFC Priority Survey](https://forms.gle/vgu13dUKTpaqWEaE9) · [💬 All Discussions](https://github.com/Drshelden/IFCV5Work/discussions) · [Decision Register](../01%20Decision%20Register/IFC5_Decision_Register.csv)*",
        "",
    ]
    return "\n".join(lines)


def build_drive_md(forms_idx, drive_idx):
    lines = [
        "# RFC Index",
        "",
        "[📝 Google Doc (this document)](https://docs.google.com/document/d/1L4wD92OdDVGm5cvcPiAGYWQBF9pDHbHXni6ohOS5rKE/edit) · [📄 GitHub MD](https://github.com/Drshelden/IFCV5Work/blob/master/02%20RFCs/README.md)",
        "",
        "41 RFCs covering the major architectural decisions for IFC5. All are at Idea status — no decisions have been made yet. ⚗️ = prototype required before Committee Review.",
        "",
        "Quick links: [📋 RFC Priority Survey](https://forms.gle/vgu13dUKTpaqWEaE9) · [💬 All GitHub Discussions](https://github.com/Drshelden/IFCV5Work/discussions) · [Decision Register](https://github.com/Drshelden/IFCV5Work/blob/master/01%20Decision%20Register/IFC5_Decision_Register.csv)",
        "",
        "---",
        "",
    ]

    for tier in TIERS:
        lines.append(f"## {tier['label']}")
        lines.append(f"*{tier['note']}*")
        lines.append("")

        for rfc_id, slug, title, proto in tier["rfcs"]:
            gh_url, gdoc_url, view_url, new_url, form_url = rfc_urls(rfc_id, slug, tier["slug"], forms_idx, drive_idx)
            proto_flag = " ⚗️" if proto else ""
            lines.append(f"**{rfc_id} — {title}{proto_flag}**")
            parts = [f"[📄 GitHub MD]({gh_url})"]
            if gdoc_url:
                parts.append(f"[📝 Google Doc]({gdoc_url})")
            parts.append(f"[💬 View discussions]({view_url})")
            parts.append(f"[+ New discussion]({new_url})")
            if form_url:
                parts.append(f"[📋 Feedback form]({form_url})")
            lines.append("   " + " · ".join(parts))
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def write_github_md(content):
    out = RFC_DIR / "README.md"
    out.write_text(content, encoding="utf-8")
    print(f"  [WRITE] {out}")


def resolve_pandoc():
    for c in ("pandoc", "pandoc.exe"):
        f = shutil.which(c)
        if f:
            return f
    for p in [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Pandoc" / "pandoc.exe",
        Path("C:/Program Files/Pandoc/pandoc.exe"),
    ]:
        if p.exists():
            return str(p)
    return None


def get_drive_service():
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
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def upload_drive(content):
    pandoc = resolve_pandoc()
    if not pandoc:
        print("  [SKIP] Drive upload — pandoc not found")
        return

    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
        f.write(content)
        md_path = f.name
    tmp_docx = md_path.replace(".md", ".docx")

    try:
        r = subprocess.run(
            [pandoc, md_path, "-o", tmp_docx, "--from", "markdown", "--to", "docx"],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            print(f"  [ERROR] Pandoc: {r.stderr}")
            return
        with open(tmp_docx, "rb") as f:
            docx_bytes = f.read()
    finally:
        for p in [md_path, tmp_docx]:
            if os.path.exists(p):
                os.unlink(p)

    from googleapiclient.http import MediaInMemoryUpload
    svc = get_drive_service()
    media = MediaInMemoryUpload(docx_bytes, mimetype=DOCX_MIME, resumable=False)
    svc.files().update(fileId=DRIVE_RFC_DOC, media_body=media, supportsAllDrives=True).execute()
    print(f"  [UPDATE] Drive RFC Index (https://docs.google.com/document/d/{DRIVE_RFC_DOC}/edit)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--md-only", action="store_true", help="Skip Drive upload")
    args = parser.parse_args()

    forms_idx, drive_idx = load_indexes()

    print("Building GitHub MD...")
    write_github_md(build_github_md(forms_idx, drive_idx))

    if not args.md_only:
        print("Building Drive version and uploading...")
        upload_drive(build_drive_md(forms_idx, drive_idx))

    print("\nDone.")


if __name__ == "__main__":
    sys.exit(main())
