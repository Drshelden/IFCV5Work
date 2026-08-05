"""
validate_example.py
-------------------
Standalone validator for IFCY JSON example files against the TypeScript schema.
Runs 7 semantic checks and prints a report to stdout.

Usage:
    python validate_example.py                          # uses defaults
    python validate_example.py path/to/file.json        # custom JSON
    python validate_example.py file.json schema.ts      # custom both

Defaults:
    JSON:   ../repo/03 Reference Examples/Hello-Wall/hello-wall-ifcy.json
    Schema: ../ifc5-layered-schema.ts
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR   = SCRIPT_DIR.parent
REPO_DIR   = WORK_DIR.parent / "repo"

UUID_RE = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE
)

# ── Schema parsing ─────────────────────────────────────────────────────────────

def parse_ts_schema(ts_path: Path) -> dict:
    text = ts_path.read_text(encoding="utf-8")
    interfaces = re.findall(r'(?:export\s+)?interface\s+(\w+)', text)
    type_aliases = re.findall(r'(?:export\s+)?type\s+(\w+)\s*=', text)
    return {"interfaces": interfaces, "type_aliases": type_aliases}

# ── JSON structure helpers ─────────────────────────────────────────────────────

def get_components(data: dict) -> list:
    d = data.get("data", [])
    return d if isinstance(d, list) else data.get("components", [])

def get_declared_prefixes(data: dict) -> set:
    schemas = data.get("schemas", {})
    return set(schemas.keys()) if isinstance(schemas, dict) else set()

def get_entity_uuids(data: dict) -> set:
    uuids = set()
    for comp in get_components(data):
        for field in ("entity", "id"):
            val = comp.get(field)
            if val and UUID_RE.match(str(val)):
                uuids.add(str(val))
    return uuids

# ── Checks ─────────────────────────────────────────────────────────────────────

def check_namespace_prefixes(data):
    declared = get_declared_prefixes(data)
    used, bad = set(), []
    for comp in get_components(data):
        t = comp.get("type", "")
        if ":" in t:
            prefix = t.split(":")[0]
            used.add(prefix)
            if prefix not in declared:
                bad.append(prefix)
    if bad:
        return "FAIL", f"Undeclared prefixes: {sorted(set(bad))}"
    if not used:
        return "WARN", "No typed components found"
    return "PASS", f"All prefixes declared: {sorted(declared)}"

def check_entity_refs(data):
    entity_uuids = get_entity_uuids(data)
    bad = []
    def walk(obj):
        if isinstance(obj, dict):
            ref = obj.get("ref")
            if ref and isinstance(ref, str) and UUID_RE.match(ref) and ref not in entity_uuids:
                bad.append(ref)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
    walk(data)
    if bad:
        uniq = list(dict.fromkeys(bad))[:3]
        return "WARN", f"{len(bad)} UUID ref(s) not matched to any entity/id — first few: {uniq}"
    total = sum(1 for _ in _iter_refs(data))
    return "PASS", f"All UUID ref values match known entities ({total} checked)"

def _iter_refs(obj):
    if isinstance(obj, dict):
        ref = obj.get("ref")
        if ref and isinstance(ref, str) and UUID_RE.match(ref):
            yield ref
        for v in obj.values():
            yield from _iter_refs(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_refs(item)

def check_spatialview_mutex(data):
    violations = []
    for comp in get_components(data):
        if "SpatialView" in comp.get("type", ""):
            attrs = comp.get("attributes", {})
            if "composedFrom" in attrs and "children" in attrs:
                violations.append(comp.get("id", "?")[:8])
    if violations:
        return "FAIL", f"SpatialView with both composedFrom and children: {violations}"
    return "PASS", "No SpatialView mutual-exclusion violations"

def check_pathlabel_location(data):
    ALLOWED = {"IfcRelAggregates", "IfcRelContainedInSpatialStructure", "SpatialView"}
    bad = []
    for comp in get_components(data):
        comp_type = comp.get("type", "")
        allowed = any(a in comp_type for a in ALLOWED)
        def walk_attrs(obj, in_allowed):
            if isinstance(obj, dict):
                if "pathLabel" in obj and not in_allowed:
                    bad.append(comp_type)
                for v in obj.values():
                    walk_attrs(v, in_allowed)
            elif isinstance(obj, list):
                for item in obj:
                    walk_attrs(item, in_allowed)
        walk_attrs(comp.get("attributes", {}), allowed)
    if bad:
        return "FAIL", f"pathLabel in non-containment components: {bad[:3]}"
    return "PASS", "pathLabel fields only in containment relation components"

def check_uuid_format(data):
    bad = []
    def walk(obj):
        if isinstance(obj, dict):
            for k in ("id", "entity"):
                v = obj.get(k)
                if v and isinstance(v, str) and not UUID_RE.match(v) and len(v) < 60:
                    bad.append(f"{k}={v!r}")
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
    walk(data)
    if bad:
        return "FAIL", f"Malformed id/entity values: {bad[:3]}"
    return "PASS", "All id/entity fields match UUID pattern"

def check_id_uniqueness(data):
    seen, dups = {}, []
    for comp in get_components(data):
        cid = comp.get("id")
        if cid:
            if cid in seen:
                dups.append(cid[:8])
            seen[cid] = True
    if dups:
        return "FAIL", f"Duplicate component ids: {dups}"
    return "PASS", f"All {len(seen)} component ids are unique"

def check_spatialview_root(data):
    entity_uuids = get_entity_uuids(data)
    bad = []
    for comp in get_components(data):
        if "SpatialView" in comp.get("type", ""):
            root = comp.get("attributes", {}).get("root", {})
            ref = root.get("ref") if isinstance(root, dict) else None
            if ref and UUID_RE.match(str(ref)) and ref not in entity_uuids:
                bad.append(f"root.ref={ref[:8]}… not found")
    if bad:
        return "FAIL", f"SpatialView root.ref not in known entities: {bad}"
    return "PASS", "All SpatialView root.ref values match known entities"

# ── Runner ─────────────────────────────────────────────────────────────────────

CHECKS = [
    ("Namespace prefix check",       check_namespace_prefixes),
    ("Entity reference check",        check_entity_refs),
    ("SpatialView mutual exclusion",  check_spatialview_mutex),
    ("pathLabel location check",      check_pathlabel_location),
    ("UUID format check",             check_uuid_format),
    ("Component id uniqueness",       check_id_uniqueness),
    ("SpatialView root ref check",    check_spatialview_root),
]

STATUS_ICON = {"PASS": "✅ PASS", "WARN": "⚠️  WARN", "FAIL": "❌ FAIL"}

def run(json_path: Path, ts_path: Path):
    print(f"\nValidating: {json_path.name}")
    print(f"Schema:     {ts_path.name}\n")

    if not json_path.exists():
        print(f"ERROR: JSON file not found: {json_path}"); sys.exit(1)
    if not ts_path.exists():
        print(f"ERROR: Schema file not found: {ts_path}"); sys.exit(1)

    data    = json.loads(json_path.read_text(encoding="utf-8"))
    ts_info = parse_ts_schema(ts_path)
    print(f"Schema: {len(ts_info['interfaces'])} interfaces, {len(ts_info['type_aliases'])} type aliases\n")

    col_w = max(len(name) for name, _ in CHECKS) + 2
    results = []
    for name, fn in CHECKS:
        status, detail = fn(data)
        results.append((name, status, detail))
        icon = STATUS_ICON.get(status, status)
        print(f"  {icon}  {name:{col_w}}  {detail}")

    counts = {s: sum(1 for _, st, _ in results if st == s) for s in ("PASS", "WARN", "FAIL")}
    overall = "FAIL" if counts["FAIL"] else ("WARN" if counts["WARN"] else "PASS")
    print(f"\n{'─'*70}")
    print(f"  Overall: {STATUS_ICON[overall]}   "
          f"{counts['PASS']} pass / {counts['WARN']} warn / {counts['FAIL']} fail\n")
    return overall

if __name__ == "__main__":
    args = sys.argv[1:]
    json_path = Path(args[0]) if len(args) >= 1 else \
        REPO_DIR / "03 Reference Examples" / "Hello-Wall" / "hello-wall-ifcy.json"
    ts_path   = Path(args[1]) if len(args) >= 2 else \
        WORK_DIR.parent / "ifc5-layered-schema.ts"

    if not json_path.is_absolute():
        json_path = (WORK_DIR / json_path).resolve()
    if not ts_path.is_absolute():
        ts_path = (WORK_DIR / ts_path).resolve()

    outcome = run(json_path, ts_path)
    sys.exit(0 if outcome in ("PASS", "WARN") else 1)
