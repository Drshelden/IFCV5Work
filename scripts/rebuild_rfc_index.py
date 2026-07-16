"""
rebuild_rfc_index.py
--------------------
Rewrites 02 RFCs/README.md cleanly with file links and discuss column.
Run this instead of the regex patch in add_rfc_links.py.
"""

import sys
from pathlib import Path

REPO      = "https://github.com/Drshelden/IFCV5Work"
BASE_PATH = "02%20RFCs"

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent
RFC_DIR    = WORK_DIR / "02 RFCs"

def row(rfc_id, slug, title, proto, tier_slug):
    file_url = f"{REPO}/blob/master/{BASE_PATH}/{slug}.md"
    list_url = f"{REPO}/discussions?discussions_q=label%3A{rfc_id}"
    new_url  = (
        f"{REPO}/discussions/new"
        f"?category={tier_slug}"
        f"&title=%5BRFC+Feedback%5D+{rfc_id}+%E2%80%94+"
        f"&labels={rfc_id}"
    )
    proto_str = "Yes" if proto else "No"
    discuss   = f"[💬 view]({list_url}) · [+ new]({new_url})"
    return f"| [{rfc_id}]({file_url}) | {title} | {proto_str} | {discuss} |"

HDR = "| ID | Title | Prototype Required? | Discuss |\n|---|---|---|---|"

TIER1 = [
    ("IFC5-001","RFC-IFC5-001-strategic-architecture-mode",       "Strategic Architecture Mode",                     False,"tier-1-foundational"),
    ("IFC5-002","RFC-IFC5-002-normative-model-formalism",         "Normative Information Model Formalism",           False,"tier-1-foundational"),
    ("IFC5-003","RFC-IFC5-003-identity-model",                    "Identity Model",                                  True, "tier-1-foundational"),
    ("IFC5-004","RFC-IFC5-004-path-model",                        "Path Model and Addressing",                       True, "tier-1-foundational"),
    ("IFC5-005","RFC-IFC5-005-namespaces",                        "Namespace and Qualified Names",                   False,"tier-1-foundational"),
    ("IFC5-006","RFC-IFC5-006-serialization-encoding",            "Serialization and Encoding",                      False,"tier-1-foundational"),
]
TIER2 = [
    ("IFC5-007","RFC-IFC5-007-scene-graph-vs-ecs",                "Scene Graph vs. ECS vs. Hybrid Architecture",     True, "tier-2-core-architecture"),
    ("IFC5-008","RFC-IFC5-008-relationship-modeling",             "Relationship Modeling Strategy",                  True, "tier-2-core-architecture"),
    ("IFC5-009","RFC-IFC5-009-class-type-representation",         "Class and Type Representation",                   False,"tier-2-core-architecture"),
    ("IFC5-010","RFC-IFC5-010-composition-inheritance",           "Composition, Inheritance, and Instancing",        True, "tier-2-core-architecture"),
    ("IFC5-011","RFC-IFC5-011-document-structure",                "Document-Level Structure",                        False,"tier-2-core-architecture"),
    ("IFC5-012","RFC-IFC5-012-modular-schema-imports",            "Modular Schema Imports",                          False,"tier-2-core-architecture"),
    ("IFC5-023","RFC-IFC5-023-attribute-representation",          "Attribute Representation",                        False,"tier-2-core-architecture"),
    ("IFC5-024","RFC-IFC5-024-type-system-primitives",            "Type System, Primitives, Enumerations, SELECTs",  False,"tier-2-core-architecture"),
    ("IFC5-025","RFC-IFC5-025-collections-cardinality",           "Collections and Cardinality",                     False,"tier-2-core-architecture"),
]
TIER3 = [
    ("IFC5-013","RFC-IFC5-013-property-sets",                     "Property Sets and Properties",                    True, "tier-3-domain-modeling"),
    ("IFC5-014","RFC-IFC5-014-geometry-architecture",             "Geometry Architecture",                           True, "tier-3-domain-modeling"),
    ("IFC5-015","RFC-IFC5-015-openusd-alignment",                 "OpenUSD Alignment",                               True, "tier-3-domain-modeling"),
    ("IFC5-016","RFC-IFC5-016-spatial-structure",                 "Spatial Structure and Decomposition",             False,"tier-3-domain-modeling"),
    ("IFC5-017","RFC-IFC5-017-material-modeling",                 "Material Modeling",                               False,"tier-3-domain-modeling"),
    ("IFC5-026","RFC-IFC5-026-openings-voids-fillings",           "Openings, Voids, and Fillings",                   True, "tier-3-domain-modeling"),
    ("IFC5-027","RFC-IFC5-027-classification-external-dictionaries","Classification and External Dictionaries",      False,"tier-3-domain-modeling"),
    ("IFC5-028","RFC-IFC5-028-units-measures",                    "Units and Measures",                              False,"tier-3-domain-modeling"),
    ("IFC5-029","RFC-IFC5-029-presentation-appearance",           "Presentation and Appearance",                     False,"tier-3-domain-modeling"),
    ("IFC5-030","RFC-IFC5-030-space-boundaries",                  "Space Boundaries and Topology",                   False,"tier-3-domain-modeling"),
    ("IFC5-031","RFC-IFC5-031-metadata-custom-data",              "Metadata and Custom Data",                        False,"tier-3-domain-modeling"),
]
TIER4 = [
    ("IFC5-018","RFC-IFC5-018-backward-compatibility",            "Backward Compatibility and Round-Tripping",       True, "tier-4-governance"),
    ("IFC5-019","RFC-IFC5-019-validation-framework",              "Validation Framework",                            False,"tier-4-governance"),
    ("IFC5-020","RFC-IFC5-020-model-views-exchange",              "Model Views and Exchange Requirements",           False,"tier-4-governance"),
    ("IFC5-021","RFC-IFC5-021-federation-external-references",    "Federation and External References",              False,"tier-4-governance"),
    ("IFC5-022","RFC-IFC5-022-versioning-schema-evolution",       "Versioning and Schema Evolution",                 False,"tier-4-governance"),
    ("IFC5-032","RFC-IFC5-032-extensibility",                     "Extensibility",                                   False,"tier-4-governance"),
    ("IFC5-033","RFC-IFC5-033-change-collaboration",              "Change, Transactions, and Collaboration",         False,"tier-4-governance"),
    ("IFC5-034","RFC-IFC5-034-performance-scale-database",        "Performance, Scale, and Database Implications",   True, "tier-4-governance"),
    ("IFC5-035","RFC-IFC5-035-web-linked-data",                   "Web and Linked-Data Alignment",                   False,"tier-4-governance"),
    ("IFC5-036","RFC-IFC5-036-ai-machine-readability",            "AI and Machine-Readability",                      False,"tier-4-governance"),
    ("IFC5-037","RFC-IFC5-037-security-trust",                    "Security and Trust",                              False,"tier-4-governance"),
    ("IFC5-038","RFC-IFC5-038-governance-conformance",            "Governance, Conformance, and Interoperability Testing",False,"tier-4-governance"),
]

def section(title, desc, rfcs):
    lines = [f"## {title}", desc, "", HDR]
    for r in rfcs:
        lines.append(row(*r))
    return "\n".join(lines)

content = f"""# RFC Index

38 RFCs covering the major architectural decisions for IFC5. All are at **Idea** status — no decisions have been made yet. The [Decision Register](../01%20Decision%20Register/IFC5_Decision_Register.csv) is the authoritative status tracker.

---

{section("Tier 1 — Foundational", "*Resolve these before anything else. All downstream RFCs depend on them.*", TIER1)}

{section("Tier 2 — Core Architecture", "*Major structural decisions. Depend on Tier 1.*", TIER2)}

{section("Tier 3 — Domain Modeling", "*Domain-specific decisions. Depend on Tier 2.*", TIER3)}

{section("Tier 4 — Process & Governance", "*Conformance, versioning, federation, and cross-cutting concerns.*", TIER4)}
"""

out = RFC_DIR / "README.md"
out.write_text(content, encoding="utf-8")
print(f"✓ Wrote {out}")
