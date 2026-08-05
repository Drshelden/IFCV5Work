"""
feedback_validate.py
--------------------
Validates the example JSON file(s) against the TypeScript schema structure
and runs semantic checks. Outputs a markdown validation report.

Usage:
    python feedback_validate.py <batch.json>
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent

UUID_RE = re.compile(
    r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
)


# ── TypeScript schema parser (regex-based) ─────────────────────────────────────

def parse_ts_schema(ts_text: str) -> dict:
    """
    Extract high-level structural information from the TypeScript schema file.
    Returns a dict with known type names, interface names, etc.
    """
    # Find all interface and type names
    interfaces = set(re.findall(r'\binterface\s+(\w+)', ts_text))
    type_aliases = set(re.findall(r'\btype\s+(\w+)\s*=', ts_text))
    # Find string literal union members (common for type discriminants)
    string_literals = set(re.findall(r'"([^"]+)"', ts_text))
    return {
        "interfaces": interfaces,
        "type_aliases": type_aliases,
        "string_literals": string_literals,
        "raw": ts_text,
    }


# ── Semantic checks ────────────────────────────────────────────────────────────

def collect_all_values(obj, key: str):
    """Recursively collect all values for a given key in a nested structure."""
    results = []
    if isinstance(obj, dict):
        if key in obj:
            results.append(obj[key])
        for v in obj.values():
            results.extend(collect_all_values(v, key))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(collect_all_values(item, key))
    return results


def collect_all_items(obj, key: str):
    """Recursively collect parent dicts that contain a given key."""
    results = []
    if isinstance(obj, dict):
        if key in obj:
            results.append(obj)
        for v in obj.values():
            results.extend(collect_all_items(v, key))
    elif isinstance(obj, list):
        for item in obj:
            results.extend(collect_all_items(item, key))
    return results


def get_components(data: dict) -> list:
    """Extract top-level components list from the JSON.
    IFCY packages use data["data"] as a flat list of components.
    """
    d = data.get("data", [])
    if isinstance(d, list):
        return d
    # fallback for alternate structures
    return data.get("components", [])


def get_declared_prefixes(data: dict) -> set:
    """Extract namespace prefixes declared in package.schemas."""
    prefixes = set()
    # In IFCY, schemas is a top-level field (no "package" wrapper)
    schemas = data.get("schemas", {})
    if isinstance(schemas, dict):
        for key in schemas:
            # key is the prefix (e.g. "ifc")
            prefixes.add(key)
    return prefixes


def get_entity_uuids(data: dict) -> set:
    """Collect all entity UUIDs from the component list.
    In IFCY, LocalRef {"ref": "uuid"} targets comp["entity"], not comp["id"].
    comp["id"] is the component's own identity for versioning/deduplication.
    """
    uuids = set()
    for comp in get_components(data):
        # Primary: the entity this component describes
        entity = comp.get("entity")
        if entity and UUID_RE.match(str(entity)):
            uuids.add(str(entity))
        # Secondary: the component's own id (some refs target components directly)
        cid = comp.get("id")
        if cid and UUID_RE.match(str(cid)):
            uuids.add(str(cid))
    return uuids


def check_namespace_prefixes(data: dict) -> tuple:
    """Check 1: every component type CURIE prefix must be declared in package.schemas."""
    declared = get_declared_prefixes(data)
    undeclared = []
    for comp in get_components(data):
        ctype = comp.get("type", "")
        if ":" in str(ctype):
            prefix = str(ctype).split(":")[0]
            if prefix not in declared:
                undeclared.append(f"`{ctype}` (prefix `{prefix}`)")
    if not declared and not get_components(data):
        return "WARN", "No components or schemas found to check"
    if undeclared:
        return "FAIL", f"Undeclared prefixes in: {', '.join(undeclared[:5])}"
    return "PASS", f"All CURIE prefixes declared in package.schemas ({declared or 'none used'})"


def check_entity_refs(data: dict) -> tuple:
    """Check 2: every {ref: uuid} value should correspond to a known entity UUID."""
    entity_uuids = get_entity_uuids(data)
    bad_refs = []
    ref_items = collect_all_items(data, "ref")
    for item in ref_items:
        ref_val = str(item["ref"])
        if UUID_RE.match(ref_val) and ref_val not in entity_uuids:
            bad_refs.append(ref_val)
    if bad_refs:
        return "WARN", f"{len(bad_refs)} ref(s) not matched to component id: {bad_refs[:3]}"
    return "PASS", f"All ref values match known component ids ({len(ref_items)} checked)"


def check_spatial_view_mutex(data: dict) -> tuple:
    """Check 3: no SpatialView component may have both composedFrom AND children."""
    violations = []
    for comp in get_components(data):
        ctype = str(comp.get("type", ""))
        if "SpatialView" in ctype or "spatialview" in ctype.lower():
            attrs = comp.get("attributes", {})
            if isinstance(attrs, dict):
                if "composedFrom" in attrs and "children" in attrs:
                    violations.append(comp.get("id", "?"))
    if violations:
        return "FAIL", f"SpatialView components with both composedFrom and children: {violations}"
    return "PASS", "No SpatialView mutual-exclusion violations found"


def check_path_label_location(data: dict) -> tuple:
    """Check 4: pathLabel fields should only appear inside IfcRelAggregates or IfcRelContainedInSpatialStructure."""
    allowed_types = {"IfcRelAggregates", "IfcRelContainedInSpatialStructure"}
    violations = []
    for comp in get_components(data):
        ctype = str(comp.get("type", ""))
        short_type = ctype.split(":")[-1] if ":" in ctype else ctype
        attrs = comp.get("attributes", {})
        if isinstance(attrs, dict) and "pathLabel" in attrs:
            if short_type not in allowed_types:
                violations.append(f"`{ctype}` (id: {comp.get('id','?')})")
    if violations:
        return "WARN", f"pathLabel found outside allowed types: {', '.join(violations[:5])}"
    return "PASS", "pathLabel fields only appear in allowed relationship types"


def check_uuid_format(data: dict) -> tuple:
    """Check 5: id and entity fields must match UUID pattern.
    Note: ref fields are excluded as they can legitimately be URIs (e.g. bSDD taxonomy URIs).
    """
    uuid_keys = {"id", "entity"}
    bad = []
    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in uuid_keys and isinstance(v, str):
                    if not UUID_RE.match(v) and len(v) > 10:
                        bad.append(f"{k}={v!r}")
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
    walk(data)
    if bad:
        return "FAIL", f"Malformed UUID values: {bad[:5]}"
    return "PASS", "All id/ref fields match UUID pattern"


def check_component_id_uniqueness(data: dict) -> tuple:
    """Check 6: no two components share the same id value."""
    seen = {}
    dupes = []
    for comp in get_components(data):
        cid = comp.get("id")
        if cid:
            if cid in seen:
                dupes.append(cid)
            seen[cid] = True
    if dupes:
        return "FAIL", f"Duplicate component ids: {dupes[:5]}"
    return "PASS", f"All {len(seen)} component ids are unique"


def check_root_ref(data: dict) -> tuple:
    """Check 7: IfcSpatialView root.ref must match an entity UUID."""
    entity_uuids = get_entity_uuids(data)
    violations = []
    for comp in get_components(data):
        ctype = str(comp.get("type", ""))
        if "SpatialView" in ctype:
            attrs = comp.get("attributes", {})
            if isinstance(attrs, dict):
                root = attrs.get("root", {})
                if isinstance(root, dict):
                    ref = root.get("ref")
                    if ref and str(ref) not in entity_uuids:
                        violations.append(f"{ref!r} (component id: {comp.get('id','?')})")
    if violations:
        return "FAIL", f"SpatialView root.ref not found in component ids: {violations[:3]}"
    return "PASS", "All SpatialView root.ref values match known component ids"


ALL_CHECKS = [
    ("Namespace prefix check",          check_namespace_prefixes),
    ("Entity reference check",          check_entity_refs),
    ("SpatialView mutual exclusion",    check_spatial_view_mutex),
    ("pathLabel location check",        check_path_label_location),
    ("UUID format check",               check_uuid_format),
    ("Component id uniqueness",         check_component_id_uniqueness),
    ("Root ref check",                  check_root_ref),
]

STATUS_ICON = {"PASS": "✅ PASS", "WARN": "⚠️ WARN", "FAIL": "❌ FAIL"}


# ── Report builder ─────────────────────────────────────────────────────────────

def validate_example(example_cfg: dict, batch_dir: Path) -> str:
    """Run all checks on one example; return a markdown section."""
    json_path = Path(example_cfg["json_path"])
    if not json_path.is_absolute():
        json_path = (WORK_DIR / json_path).resolve()
    ts_path = Path(example_cfg.get("schema_ts_path", ""))
    if ts_path and not ts_path.is_absolute():
        ts_path = (WORK_DIR / ts_path).resolve()

    lines = [f"### Example: `{example_cfg['id']}`\n"]
    lines.append(f"**JSON file:** `{json_path}`  ")
    lines.append(f"**Schema:** `{ts_path}`\n")

    if not json_path.exists():
        lines.append(f"**ERROR:** JSON file not found: `{json_path}`\n")
        return "\n".join(lines)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as exc:
        lines.append(f"**ERROR:** Could not parse JSON: {exc}\n")
        return "\n".join(lines)

    # Parse TS schema if available
    ts_info = {}
    if ts_path and ts_path.exists():
        ts_info = parse_ts_schema(ts_path.read_text(encoding="utf-8", errors="replace"))
        lines.append(f"*Schema interfaces found: {len(ts_info['interfaces'])}; "
                     f"type aliases: {len(ts_info['type_aliases'])}*\n")
    else:
        lines.append("*Schema file not found — structural checks only.*\n")

    # Run semantic checks
    lines.append("| Check | Status | Detail |")
    lines.append("|-------|--------|--------|")
    overall = "PASS"
    for name, fn in ALL_CHECKS:
        try:
            status, detail = fn(data)
        except Exception as exc:
            status, detail = "WARN", f"Check error: {exc}"
        icon = STATUS_ICON.get(status, status)
        lines.append(f"| {name} | {icon} | {detail} |")
        if status == "FAIL":
            overall = "FAIL"
        elif status == "WARN" and overall == "PASS":
            overall = "WARN"

    lines.append(f"\n**Overall result:** {STATUS_ICON.get(overall, overall)}")
    return "\n".join(lines)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate IFC5 example files against schema.")
    parser.add_argument("batch_json", help="Path to batch.json")
    args = parser.parse_args()

    batch_path = Path(args.batch_json).resolve()
    if not batch_path.exists():
        print(f"[validate] ERROR: batch.json not found: {batch_path}")
        sys.exit(1)

    cfg = json.loads(batch_path.read_text(encoding="utf-8"))
    batch_dir = batch_path.parent
    batch_id = cfg["batch_id"]

    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    examples = cfg.get("validate_examples", [])
    if not examples:
        print("[validate] No validate_examples in batch config — nothing to validate.")
        sys.exit(0)

    sections = [
        f"# Validation Report — Batch {batch_id}",
        f"**Generated:** {now}  ",
        f"**Examples validated:** {len(examples)}\n",
    ]

    print(f"[validate] Batch: {batch_id}  |  {len(examples)} example(s) to validate")

    for ex in examples:
        print(f"[validate]   → {ex['id']} ...", end=" ", flush=True)
        try:
            section = validate_example(ex, batch_dir)
            sections.append(section)
            print("OK")
        except Exception as exc:
            sections.append(f"### Example: `{ex['id']}`\n**ERROR:** {exc}\n")
            print(f"ERROR: {exc}")

    report_path = batch_dir / "validation-report.md"
    report_path.write_text("\n\n".join(sections), encoding="utf-8")
    print(f"[validate] Report written → {report_path.relative_to(WORK_DIR)}")


if __name__ == "__main__":
    main()
