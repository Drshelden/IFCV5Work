"""
add_rfc_links.py
----------------
Adds a discussion header and footer to each of the 38 RFC markdown files,
and updates 02 RFCs/README.md with a Discuss column.

Run once. Safe to re-run — detects already-patched files and skips them.

Usage:
    python add_rfc_links.py [--dry-run]
"""

import argparse
import re
import sys
from pathlib import Path

REPO = "https://github.com/Drshelden/IFCV5Work"

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent
RFC_DIR    = WORK_DIR / "02 RFCs"

# ── RFC metadata ───────────────────────────────────────────────────────────────
# (id, slug, title, tier_slug, tier_label)
RFCS = [
    ("IFC5-001", "RFC-IFC5-001-strategic-architecture-mode",        "Strategic Architecture Mode",                        "tier-1-foundational",      "Tier 1 — Foundational"),
    ("IFC5-002", "RFC-IFC5-002-normative-model-formalism",          "Normative Information Model Formalism",              "tier-1-foundational",      "Tier 1 — Foundational"),
    ("IFC5-003", "RFC-IFC5-003-identity-model",                     "Identity Model",                                     "tier-1-foundational",      "Tier 1 — Foundational"),
    ("IFC5-004", "RFC-IFC5-004-path-model",                         "Path Model and Addressing",                          "tier-1-foundational",      "Tier 1 — Foundational"),
    ("IFC5-005", "RFC-IFC5-005-namespaces",                         "Namespace and Qualified Names",                      "tier-1-foundational",      "Tier 1 — Foundational"),
    ("IFC5-006", "RFC-IFC5-006-serialization-encoding",             "Serialization and Encoding",                         "tier-1-foundational",      "Tier 1 — Foundational"),
    ("IFC5-007", "RFC-IFC5-007-scene-graph-vs-ecs",                 "Scene Graph vs. ECS vs. Hybrid Architecture",        "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-008", "RFC-IFC5-008-relationship-modeling",              "Relationship Modeling Strategy",                     "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-009", "RFC-IFC5-009-class-type-representation",          "Class and Type Representation",                      "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-010", "RFC-IFC5-010-composition-inheritance",            "Composition, Inheritance, and Instancing",           "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-011", "RFC-IFC5-011-document-structure",                 "Document-Level Structure",                           "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-012", "RFC-IFC5-012-modular-schema-imports",             "Modular Schema Imports",                             "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-013", "RFC-IFC5-013-property-sets",                      "Property Sets and Properties",                       "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-014", "RFC-IFC5-014-geometry-architecture",              "Geometry Architecture",                              "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-015", "RFC-IFC5-015-openusd-alignment",                  "OpenUSD Alignment",                                  "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-016", "RFC-IFC5-016-spatial-structure",                  "Spatial Structure and Decomposition",                "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-017", "RFC-IFC5-017-material-modeling",                  "Material Modeling",                                  "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-018", "RFC-IFC5-018-backward-compatibility",             "Backward Compatibility and Round-Tripping",          "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-019", "RFC-IFC5-019-validation-framework",               "Validation Framework",                               "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-020", "RFC-IFC5-020-model-views-exchange",               "Model Views and Exchange Requirements",              "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-021", "RFC-IFC5-021-federation-external-references",     "Federation and External References",                 "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-022", "RFC-IFC5-022-versioning-schema-evolution",        "Versioning and Schema Evolution",                    "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-023", "RFC-IFC5-023-attribute-representation",           "Attribute Representation",                           "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-024", "RFC-IFC5-024-type-system-primitives",             "Type System, Primitives, Enumerations, SELECTs",     "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-025", "RFC-IFC5-025-collections-cardinality",            "Collections and Cardinality",                        "tier-2-core-architecture", "Tier 2 — Core Architecture"),
    ("IFC5-026", "RFC-IFC5-026-openings-voids-fillings",            "Openings, Voids, and Fillings",                      "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-027", "RFC-IFC5-027-classification-external-dictionaries","Classification and External Dictionaries",          "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-028", "RFC-IFC5-028-units-measures",                     "Units and Measures",                                 "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-029", "RFC-IFC5-029-presentation-appearance",            "Presentation and Appearance",                        "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-030", "RFC-IFC5-030-space-boundaries",                   "Space Boundaries and Topology",                      "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-031", "RFC-IFC5-031-metadata-custom-data",               "Metadata and Custom Data",                           "tier-3-domain-modeling",   "Tier 3 — Domain Modeling"),
    ("IFC5-032", "RFC-IFC5-032-extensibility",                      "Extensibility",                                      "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-033", "RFC-IFC5-033-change-collaboration",               "Change, Transactions, and Collaboration",            "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-034", "RFC-IFC5-034-performance-scale-database",         "Performance, Scale, and Database Implications",      "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-035", "RFC-IFC5-035-web-linked-data",                    "Web and Linked-Data Alignment",                      "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-036", "RFC-IFC5-036-ai-machine-readability",             "AI and Machine-Readability",                         "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-037", "RFC-IFC5-037-security-trust",                     "Security and Trust",                                 "tier-4-governance",        "Tier 4 — Governance"),
    ("IFC5-038", "RFC-IFC5-038-governance-conformance",             "Governance, Conformance, and Interoperability Testing","tier-4-governance",      "Tier 4 — Governance"),
]

SENTINEL = "<!-- rfc-links -->"

def make_header(rfc_id, title, tier_slug, tier_label, slug):
    file_url  = f"{REPO}/blob/master/02%20RFCs/{slug}.md"
    new_url   = (
        f"{REPO}/discussions/new"
        f"?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}"
    )
    list_url  = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"

    return (
        f"{SENTINEL}\n"
        f"> **{rfc_id} — {title}** · {tier_label}\n"
        f"> \n"
        f"> 💬 [View all discussions on this RFC]({list_url}) &nbsp;|&nbsp; "
        f"[+ Start a new discussion]({new_url})\n\n"
    )

def make_footer(rfc_id, title, tier_slug, tier_label, slug):
    new_url  = (
        f"{REPO}/discussions/new"
        f"?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}"
    )
    list_url = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"
    index_url = f"{REPO}/blob/master/02%20RFCs/README.md"

    return (
        f"\n\n---\n\n{SENTINEL}\n"
        f"💬 **Discuss this RFC:** "
        f"[View existing discussions]({list_url}) &nbsp;|&nbsp; "
        f"[Start a new discussion]({new_url})\n\n"
        f"← [Back to RFC Index]({index_url})\n"
    )


def patch_file(path: Path, header: str, footer: str, dry_run: bool) -> str:
    content = path.read_text(encoding="utf-8")

    if SENTINEL in content:
        return "SKIP"

    new_content = header + content + footer

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return "PATCH"


def update_index(dry_run: bool):
    index_path = RFC_DIR / "README.md"
    content = index_path.read_text(encoding="utf-8")

    if "Discuss" in content and SENTINEL in content:
        print("  [SKIP] README.md already patched")
        return

    # Add Discuss column to each table row
    # Pattern: | IFC5-XXX | Title | Yes/No |
    def add_discuss_col(m):
        rfc_id = m.group(1).strip()
        rest   = m.group(2)
        list_url = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"
        new_url_map = {r[0]: (
            f"{REPO}/discussions/new"
            f"?category={r[3]}"
            f"&title=%5BRFC+Feedback%5D+{r[0]}+%E2%80%94+"
            f"&labels={r[0]}"
        ) for r in RFCS}
        new_url = new_url_map.get(rfc_id, "#")
        return f"| [{rfc_id}]{rest}| [💬 view]({list_url}) · [+ new]({new_url}) |"

    # Add header column to separator rows: |---|---|---|  →  |---|---|---|---|
    new_content = re.sub(
        r'\| (IFC5-\d+) (\|[^|]+\|[^|]+\|)',
        add_discuss_col,
        content
    )
    # Add Discuss to table headers
    new_content = new_content.replace(
        "| ID | Title | Prototype Required? |",
        "| ID | Title | Prototype Required? | Discuss |"
    )
    # Add separator column
    new_content = new_content.replace(
        "|---|---|---|",
        "|---|---|---|---|"
    )

    print(f"  [PATCH] README.md")
    if not dry_run:
        index_path.write_text(new_content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        print("=== DRY RUN ===\n")

    for rfc_id, slug, title, tier_slug, tier_label in RFCS:
        path = RFC_DIR / f"{slug}.md"
        if not path.exists():
            print(f"  [WARN] Not found: {path.name}")
            continue

        header = make_header(rfc_id, title, tier_slug, tier_label, slug)
        footer = make_footer(rfc_id, title, tier_slug, tier_label, slug)
        result = patch_file(path, header, footer, dry_run=args.dry_run)
        print(f"  [{result}] {path.name}")

    print()
    update_index(dry_run=args.dry_run)
    print("\n✓ Done.")


if __name__ == "__main__":
    sys.exit(main())
