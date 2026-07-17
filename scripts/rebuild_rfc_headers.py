"""
rebuild_rfc_headers.py
----------------------
Replaces the header and footer of every RFC .md file with a 3x2 HTML table:

  Row 1: [GitHub MD]          [Google Doc]
  Row 2: [View discussions]   [New discussion]
  Row 3: [📋 Take feedback form]   (colspan=2)

Uses HTML table so the form row can span both columns (GitHub renders HTML in .md).

Usage:
    python rebuild_rfc_headers.py [--dry-run]
"""

import argparse
import json
import re
import sys
import urllib.parse
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
WORK_DIR    = SCRIPT_DIR.parent
RFC_DIR     = WORK_DIR / "02 RFCs"
FORMS_INDEX = SCRIPT_DIR / "forms_index.json"
DRIVE_INDEX = SCRIPT_DIR / "drive_index.json"

REPO = "https://github.com/Drshelden/IFCV5Work"

BODY_TEMPLATE = """\
**Comment type:** Editorial | Technical Defect | Semantic Concern | Compatibility Concern | Alternative Proposal | Evidence | Blocking Objection | General Support

*(delete all but one)*

---

**Feedback:**

<!-- Be specific — reference section numbers or quote RFC text where relevant -->

---

**Supporting evidence or examples:**

<!-- Optional: links, code, schema examples, prior art -->

---

**Questions for the working group:**

<!-- Optional: number each question Q1, Q2, ... -->
"""
ENCODED_BODY = urllib.parse.quote(BODY_TEMPLATE, safe="")

RFCS = [
    ("IFC5-001","RFC-IFC5-001-strategic-architecture-mode",       "-tier-1-foundational"),
    ("IFC5-002","RFC-IFC5-002-normative-model-formalism",         "-tier-1-foundational"),
    ("IFC5-003","RFC-IFC5-003-identity-model",                    "-tier-1-foundational"),
    ("IFC5-004","RFC-IFC5-004-path-model",                        "-tier-1-foundational"),
    ("IFC5-005","RFC-IFC5-005-namespaces",                        "-tier-1-foundational"),
    ("IFC5-006","RFC-IFC5-006-serialization-encoding",            "-tier-1-foundational"),
    ("IFC5-007","RFC-IFC5-007-scene-graph-vs-ecs",                "-tier-2-core-architecture"),
    ("IFC5-008","RFC-IFC5-008-relationship-modeling",             "-tier-2-core-architecture"),
    ("IFC5-009","RFC-IFC5-009-class-type-representation",         "-tier-2-core-architecture"),
    ("IFC5-010","RFC-IFC5-010-composition-inheritance",           "-tier-2-core-architecture"),
    ("IFC5-011","RFC-IFC5-011-document-structure",                "-tier-2-core-architecture"),
    ("IFC5-012","RFC-IFC5-012-modular-schema-imports",            "-tier-2-core-architecture"),
    ("IFC5-013","RFC-IFC5-013-property-sets",                     "-tier-3-domain-modeling"),
    ("IFC5-014","RFC-IFC5-014-geometry-architecture",             "-tier-3-domain-modeling"),
    ("IFC5-015","RFC-IFC5-015-openusd-alignment",                 "-tier-3-domain-modeling"),
    ("IFC5-016","RFC-IFC5-016-spatial-structure",                 "-tier-3-domain-modeling"),
    ("IFC5-017","RFC-IFC5-017-material-modeling",                 "-tier-3-domain-modeling"),
    ("IFC5-018","RFC-IFC5-018-backward-compatibility",            "-tier-4-governance"),
    ("IFC5-019","RFC-IFC5-019-validation-framework",              "-tier-4-governance"),
    ("IFC5-020","RFC-IFC5-020-model-views-exchange",              "-tier-4-governance"),
    ("IFC5-021","RFC-IFC5-021-federation-external-references",    "-tier-4-governance"),
    ("IFC5-022","RFC-IFC5-022-versioning-schema-evolution",       "-tier-4-governance"),
    ("IFC5-023","RFC-IFC5-023-attribute-representation",          "-tier-2-core-architecture"),
    ("IFC5-024","RFC-IFC5-024-type-system-primitives",            "-tier-2-core-architecture"),
    ("IFC5-025","RFC-IFC5-025-collections-cardinality",           "-tier-2-core-architecture"),
    ("IFC5-026","RFC-IFC5-026-openings-voids-fillings",           "-tier-3-domain-modeling"),
    ("IFC5-027","RFC-IFC5-027-classification-external-dictionaries","-tier-3-domain-modeling"),
    ("IFC5-028","RFC-IFC5-028-units-measures",                    "-tier-3-domain-modeling"),
    ("IFC5-029","RFC-IFC5-029-presentation-appearance",           "-tier-3-domain-modeling"),
    ("IFC5-030","RFC-IFC5-030-space-boundaries",                  "-tier-3-domain-modeling"),
    ("IFC5-031","RFC-IFC5-031-metadata-custom-data",              "-tier-3-domain-modeling"),
    ("IFC5-032","RFC-IFC5-032-extensibility",                     "-tier-4-governance"),
    ("IFC5-033","RFC-IFC5-033-change-collaboration",              "-tier-4-governance"),
    ("IFC5-034","RFC-IFC5-034-performance-scale-database",        "-tier-4-governance"),
    ("IFC5-035","RFC-IFC5-035-web-linked-data",                   "-tier-4-governance"),
    ("IFC5-036","RFC-IFC5-036-ai-machine-readability",            "-tier-4-governance"),
    ("IFC5-037","RFC-IFC5-037-security-trust",                    "-tier-4-governance"),
    ("IFC5-038","RFC-IFC5-038-governance-conformance",            "-tier-4-governance"),
]

SENTINEL_LINKS = "<!-- rfc-links -->"
SENTINEL_FORM  = "<!-- rfc-form -->"
SENTINEL_NAV   = "<!-- rfc-nav -->"


def make_grid(rfc_id, slug, tier_slug, gdoc_url, form_url):
    github_url = f"{REPO}/blob/master/02%20RFCs/{slug}.md"
    list_url   = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"
    new_url    = (
        f"{REPO}/discussions/new"
        f"?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}"
        f"&body={ENCODED_BODY}"
    )

    # Plain markdown links — renders on GitHub and converts to Word hyperlinks via Pandoc
    return (
        f"{SENTINEL_NAV}\n"
        f"[📄 GitHub MD]({github_url}) · "
        f"[📝 Google Doc]({gdoc_url}) · "
        f"[💬 View all discussions]({list_url}) · "
        f"[+ New discussion]({new_url}) · "
        f"[📋 Take the feedback form]({form_url})\n"
    )


def strip_old_blocks(content):
    """Remove all existing sentinel-bounded link/form/nav blocks."""
    # Remove <!-- rfc-nav --> lines (markdown link line or HTML table block)
    content = re.sub(
        r'<!-- rfc-nav -->.*?(?=\n\n# |\n\n---|\n\n\S|\Z)',
        '', content, flags=re.DOTALL
    )
    # Remove <!-- rfc-links --> blocks
    content = re.sub(r'<!-- rfc-links -->.*?\n\n', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- rfc-links -->[^\n]*\n', '', content)
    # Remove <!-- rfc-form --> line (with or without blank line after)
    content = re.sub(r'<!-- rfc-form -->[^\n]*\n[^\n]*\n?', '', content)
    # Remove old "💬 Discuss this RFC:" inline blocks
    content = re.sub(r'💬 \*\*Discuss this RFC:\*\*[^\n]*\n', '', content)
    # Remove | Source Topics | ... | rows from metadata tables
    content = re.sub(r'\| \*\*Source Topics\*\* \|[^\n]*\n', '', content)
    # Remove trailing ---\n before cleaned footer
    content = re.sub(r'\n---\n\n$', '\n', content)
    return content.strip()


def patch_file(md_path, grid_block, dry_run):
    content = md_path.read_text(encoding="utf-8")
    clean   = strip_old_blocks(content)
    new_content = grid_block + "\n\n" + clean + "\n\n---\n\n" + grid_block
    if not dry_run:
        md_path.write_text(new_content, encoding="utf-8")
    return "PATCH"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    forms_index = {}
    if FORMS_INDEX.exists():
        forms_index = json.loads(FORMS_INDEX.read_text(encoding="utf-8"))

    drive_index = {}
    if DRIVE_INDEX.exists():
        drive_index = json.loads(DRIVE_INDEX.read_text(encoding="utf-8"))

    for rfc_id, slug, tier_slug in RFCS:
        md_path = RFC_DIR / f"{slug}.md"
        if not md_path.exists():
            print(f"  [WARN] {rfc_id}: file not found")
            continue

        # Google Doc URL
        drive_key = f"02 RFCs\\{slug}.md"
        doc_id    = drive_index.get(drive_key) or drive_index.get(drive_key.replace("\\", "/"))
        gdoc_url  = f"https://docs.google.com/document/d/{doc_id}/edit" if doc_id else "#"

        # Form URL
        form_entry = forms_index.get(rfc_id, {})
        form_url   = form_entry.get("url", "#")

        grid = make_grid(rfc_id, slug, tier_slug, gdoc_url, form_url)
        result = patch_file(md_path, grid, dry_run=args.dry_run)
        print(f"  [{result}] {rfc_id}")

    print("\n✓ Done. Run sync_and_push.bat to push to GitHub and update Google Docs.")


if __name__ == "__main__":
    sys.exit(main())
